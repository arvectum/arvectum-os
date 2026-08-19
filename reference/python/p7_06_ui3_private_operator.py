#!/usr/bin/env python3
"""P7.06-UI3 persistent private operator access with bounded UI4 preflight.

Owner-local, exact-release and reversible. UI3 provides the supervised loopback
process, owner-local ingress secret/process session and existing exact P7.04
technical access. UI4 adds one preflight-only route over real retained state.
Neither layer creates Organizational Authority, consequential approval or a
canonical mutation shortcut.
"""
from __future__ import annotations

import argparse, hmac, json, os, secrets, tempfile
from dataclasses import dataclass
from http import HTTPStatus
from http.cookies import SimpleCookie
from pathlib import Path
from typing import Any, Mapping, Optional
from urllib.parse import parse_qs, urlsplit

from arvectum_os_ref.identity import Identity
import p7_04_persistent_access as p704
import p7_06_governed_deploy as p706
import p7_06_ui1_live_workspace as ui1
import p7_06_ui2_governed_interaction as ui2
import p7_06_ui4_owner_preflight as ui4

SCHEMA="arvectum.p7_06_ui3.private-operator/1"
MODE="Persistent Internal / owner-operated"
HOST="127.0.0.1"; PORT=8765; MIN_PORT=1024; MAX_PORT=65535
COOKIE="arvectum_ui3_session"; UNLOCK="/ui3/unlock"
MAX_CONFIG=16384; MAX_FORM=4096; SECRET_BYTES=48
LEGACY_PROVIDER="none-until-p7-06-ui4"
UI4_PROVIDER="p7-06-ui4-preflight-only"

class UI3Error(RuntimeError): pass
class UI3BoundaryError(UI3Error): pass
class UI3IntegrityError(UI3Error): pass
class UI3AccessDenied(UI3Error): pass

@dataclass(frozen=True, slots=True)
class Config:
    host: str; port: int; credential_id: Optional[str]

@dataclass(frozen=True, slots=True)
class Access:
    organization: Identity; principal: Identity; credential_id: str
    credential_file: Path; inspect_grant_id: str; interaction_grant_id: str

def _config(root: Path)->Path: return root.expanduser().resolve()/"config"/"p7-06-ui3.json"
def _secret(root: Path)->Path: return root.expanduser().resolve()/"secrets"/"p7-06-ui3"/"access.secret"

def _owner_file(path: Path, label: str, limit: int)->None:
    if path.is_symlink() or not path.is_file(): raise UI3IntegrityError(f"{label} missing or unsafe")
    if path.stat().st_size>limit: raise UI3IntegrityError(f"{label} too large")
    if os.name!="nt" and path.stat().st_mode & 0o077: raise UI3IntegrityError(f"{label} is not owner-only")

def _atomic(path: Path, text: str, *, exclusive=False)->None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.name!="nt": os.chmod(path.parent,0o700)
    if exclusive and path.exists(): raise UI3IntegrityError("refusing to replace existing secret")
    fd,tmp=tempfile.mkstemp(prefix=f".{path.name}.",dir=path.parent)
    try:
        if os.name!="nt": os.fchmod(fd,0o600)
        with os.fdopen(fd,"w",encoding="utf-8") as h:
            h.write(text); h.flush(); os.fsync(h.fileno())
        if exclusive and path.exists(): raise UI3IntegrityError("refusing to replace existing secret")
        os.replace(tmp,path)
        if os.name!="nt": os.chmod(path,0o600)
    finally:
        try: os.unlink(tmp)
        except FileNotFoundError: pass

def _listener(host: str, port: int)->tuple[str,int]:
    try: host=ui1._verify_loopback_host(host)
    except (ui1.UI1Error, TypeError) as exc: raise UI3BoundaryError("explicit IPv4 loopback required") from exc
    if host!=HOST: raise UI3BoundaryError("persistent listener is pinned to 127.0.0.1")
    if isinstance(port,bool) or not isinstance(port,int) or not MIN_PORT<=port<=MAX_PORT:
        raise UI3BoundaryError("non-privileged bounded port required")
    return host,port

def _cid(value: Optional[str])->Optional[str]:
    if value is None: return None
    value=value.strip()
    if not value or len(value)>128 or any(c in value for c in "\r\n/\\\0"):
        raise UI3BoundaryError("invalid credential id")
    return value

def _read_secret(path: Path)->str:
    _owner_file(path,"UI3 ingress secret",4096)
    value=path.read_text(encoding="utf-8")
    if value.endswith("\n"): value=value[:-1]
    if not value or "\n" in value or "\r" in value: raise UI3IntegrityError("invalid ingress secret")
    return value

def _mapping(path: Path)->dict[str,Any]:
    _owner_file(path,"UI3 configuration",MAX_CONFIG)
    try: value=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: raise UI3IntegrityError("unreadable UI3 configuration") from exc
    keys={"schema","operating_mode","listener_host","listener_port","credential_id","listener_scope","ingress_authentication","interaction_provider","organizational_authority_provided","consequential_approval_provided","canonical_mutation_performed"}
    if not isinstance(value,dict) or set(value)!=keys: raise UI3IntegrityError("invalid UI3 configuration shape")
    if value["schema"]!=SCHEMA or value["operating_mode"]!=MODE: raise UI3IntegrityError("invalid UI3 configuration identity")
    if value["listener_scope"]!="ipv4-loopback-only" or value["ingress_authentication"]!="owner-local-secret-to-process-session": raise UI3IntegrityError("invalid private ingress mode")
    if value["interaction_provider"] not in {LEGACY_PROVIDER,UI4_PROVIDER}: raise UI3IntegrityError("invalid bounded interaction provider mode")
    if any(value[k] is not False for k in ("organizational_authority_provided","consequential_approval_provided","canonical_mutation_performed")): raise UI3IntegrityError("UI3/UI4 may not claim authority/approval/mutation")
    _listener(value["listener_host"],value["listener_port"]); _cid(value["credential_id"])
    return value

def load_config(root: Path)->Config:
    v=_mapping(_config(root)); return Config(v["listener_host"],v["listener_port"],v["credential_id"])

def _identity(raw: Mapping[str,Any])->Identity:
    try: return Identity(str(raw["namespace"]),str(raw["value"]),str(raw["scope"]))
    except Exception as exc: raise UI3IntegrityError("invalid access identity") from exc

def _grant(state: Mapping[str,Any], key: str, operation: str, resource: str)->bool:
    org=state["organization"]
    return any(g["principal_key"]==key and g["organization"]==org and g["operation"]==operation and g["resource"]==resource and g["access_paths"]==["local"] and g["status"]=="active" for g in state["grants"].values())

def resolve_operator_access(root: Path, credential_id: Optional[str]=None)->Access:
    root=root.expanduser().resolve(); credential_id=_cid(credential_id)
    try: p704.verify_store(root); state=p704.load_access_store(root)
    except p704.P704Error as exc: raise UI3AccessDenied("P7.04 access state unavailable") from exc
    candidates=[]
    for cid,c in state["credentials"].items():
        if credential_id is not None and cid!=credential_id: continue
        p=state["principals"].get(c["principal_key"])
        if c["status"]!="active" or not p or p["status"]!="enabled" or p["kind"]!="human": continue
        if _grant(state,c["principal_key"],ui1.WORKSPACE_OPERATION,ui1.WORKSPACE_RESOURCE) and _grant(state,c["principal_key"],ui2.INTERACTION_OPERATION,ui2.INTERACTION_RESOURCE): candidates.append((cid,c["principal_key"]))
    if len(candidates)!=1: raise UI3AccessDenied("exactly one selected human credential with exact UI1/UI2 grants is required")
    cid,key=candidates[0]; org=_identity(state["organization"]); principal=_identity(state["principals"][key]["identity"]); cred=root/"secrets"/"p7-04"/f"{cid}.secret"
    try:
        inspect=ui1._authorize(root,organization=org,principal=principal,credential_id=cid,credential_file=cred)
        interact=ui2._authorize_interaction(root,organization=org,principal=principal,credential_id=cid,credential_file=cred)
    except (ui1.UI1Error,ui2.UI2Error) as exc: raise UI3AccessDenied("P7.04 exact grant re-check failed") from exc
    return Access(org,principal,cid,cred,inspect.grant_id,interact.grant_id)

def initialize_private_access(root: Path, *, host=HOST, port=PORT, credential_id: Optional[str]=None)->dict[str,Any]:
    root=root.expanduser().resolve(); host,port=_listener(host,port); credential_id=_cid(credential_id)
    desired={"schema":SCHEMA,"operating_mode":MODE,"listener_host":host,"listener_port":port,"credential_id":credential_id,"listener_scope":"ipv4-loopback-only","ingress_authentication":"owner-local-secret-to-process-session","interaction_provider":UI4_PROVIDER,"organizational_authority_provided":False,"consequential_approval_provided":False,"canonical_mutation_performed":False}
    path=_config(root)
    if path.exists():
        existing=_mapping(path)
        legacy=dict(desired); legacy["interaction_provider"]=LEGACY_PROVIDER
        if existing==legacy:
            _atomic(path,json.dumps(desired,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
        elif existing!=desired:
            raise UI3IntegrityError("existing UI3 configuration differs; explicit uninstall/reconfigure required")
    else: _atomic(path,json.dumps(desired,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    secret=_secret(root)
    if secret.exists(): _read_secret(secret)
    else: _atomic(secret,secrets.token_urlsafe(SECRET_BYTES)+"\n",exclusive=True); _read_secret(secret)
    return {"status":"PASS","listener":f"{host}:{port}","credential_id":credential_id,"secret_returned":False,"ui4_preflight_enabled":True,"organizational_authority_provided":False,"canonical_mutation_performed":False}

def rotate_access_secret(root: Path)->dict[str,Any]:
    _mapping(_config(root)); _read_secret(_secret(root)); _atomic(_secret(root),secrets.token_urlsafe(SECRET_BYTES)+"\n")
    return {"status":"PASS","prior_sessions_invalidated":True,"secret_returned":False}

def remove_private_material(root: Path)->None:
    _config(root).unlink(missing_ok=True); _secret(root).unlink(missing_ok=True)
    try: _secret(root).parent.rmdir()
    except OSError: pass

def verify_exact_release(root: Path)->str:
    root=root.expanduser().resolve(); rel=p706.current_release(root); p706.verify_release(root,rel)
    base=root/"releases"/rel/"source"/"reference"/"python"
    for module in (Path(__file__),Path(p706.__file__),Path(ui1.__file__),Path(ui2.__file__),Path(ui4.__file__)):
        pinned=base/module.name
        if not pinned.is_file() or pinned.is_symlink() or module.resolve()!=pinned.resolve(): raise UI3IntegrityError(f"exact-release module pin failed: {module.name}")
    return rel

def verify_private_access(root: Path, *, exact=False)->dict[str,Any]:
    cfg=load_config(root); config=_mapping(_config(root)); _read_secret(_secret(root)); access=resolve_operator_access(root,cfg.credential_id)
    return {"status":"PASS","listener":f"{cfg.host}:{cfg.port}","release_sha":verify_exact_release(root) if exact else None,"credential_id":access.credential_id,"inspect_grant_id":access.inspect_grant_id,"interaction_grant_id":access.interaction_grant_id,"ui4_preflight_enabled":config["interaction_provider"]==UI4_PROVIDER,"organizational_authority_provided":False,"consequential_approval_provided":False,"canonical_mutation_performed":False}

def _cookie(header: Optional[str])->Optional[str]:
    if not header: return None
    try: jar=SimpleCookie(); jar.load(header)
    except Exception: return None
    item=jar.get(COOKIE); return item.value if item else None

def _unlock_html(csrf: str, failed=False)->str:
    alert='<p role="alert">Access denied.</p>' if failed else ""
    return f'<!doctype html><html><head><meta charset="utf-8"><title>Arvectum OS private operator access</title></head><body><main><h1>Private operator access</h1><p>Owner-local unlock only. This grants no Organizational Authority or approval.</p>{alert}<form method="post" action="{UNLOCK}"><input type="hidden" name="csrf" value="{csrf}"><label>Access secret <input type="password" name="access_secret" required autocomplete="off"></label><button type="submit">Unlock</button></form></main></body></html>'

def _form(handler: Any)->dict[str,str]:
    if handler.headers.get("Content-Type","").split(";",1)[0].strip().lower()!="application/x-www-form-urlencoded": raise UI3BoundaryError("bounded form required")
    try: length=int(handler.headers.get("Content-Length",""))
    except ValueError as exc: raise UI3BoundaryError("invalid form length") from exc
    if not 0<length<=MAX_FORM: raise UI3BoundaryError("form outside bounded size")
    try: values=parse_qs(handler.rfile.read(length).decode("utf-8"),keep_blank_values=True,strict_parsing=True)
    except (UnicodeDecodeError,ValueError) as exc: raise UI3BoundaryError("invalid form") from exc
    if set(values)!={"csrf","access_secret"} or any(len(v)!=1 for v in values.values()): raise UI3BoundaryError("unexpected form fields")
    result={k:v[0] for k,v in values.items()}
    if not result["csrf"] or not result["access_secret"] or len(result["access_secret"])>512: raise UI3BoundaryError("invalid form values")
    return result

def make_private_server(root: Path):
    root=root.expanduser().resolve(); rel=verify_exact_release(root); cfg=load_config(root); config=_mapping(_config(root)); access=resolve_operator_access(root,cfg.credential_id); ingress=_read_secret(_secret(root))
    if config["interaction_provider"]!=UI4_PROVIDER: raise UI3IntegrityError("UI4 preflight provider has not been activated by exact-release init")
    # UI2's canonical-mutation interaction provider intentionally remains empty.
    # UI4 is a separate preflight-only route and cannot manufacture a candidate.
    server=ui2.make_server(host=cfg.host,port=cfg.port,root=root,organization=access.organization,principal=access.principal,credential_id=access.credential_id,credential_file=access.credential_file,interaction_provider=lambda _interaction_id: None)
    base=server.RequestHandlerClass; session=secrets.token_urlsafe(SECRET_BYTES); csrf=secrets.token_urlsafe(32); ui4_csrf=secrets.token_urlsafe(32)
    class Handler(base):
        def _auth(self):
            value=_cookie(self.headers.get("Cookie")); return bool(value) and hmac.compare_digest(value,session)
        def _unlock(self,status=HTTPStatus.OK,failed=False,body=True):
            payload=_unlock_html(csrf,failed).encode(); self.send_response(status.value); ui2._security_headers(self); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(payload))); self.end_headers()
            if body: self.wfile.write(payload)
        def _gate(self,body=True):
            try: ui2._require_loopback_host(self)
            except ui2.UI2BoundaryError: self._unlock(HTTPStatus.BAD_REQUEST,body=body); return False
            if not self._auth(): self._unlock(HTTPStatus.UNAUTHORIZED,body=body); return False
            return True
        def _ui4(self, *, ran=False):
            try:
                preflight=ui4.build_owner_preflight(root,organization=access.organization,principal=access.principal,credential_id=access.credential_id,credential_file=access.credential_file)
                if ran: ui4.record_browser_preflight(root,preflight)
                ui4.write_html(self,HTTPStatus.OK,ui4.render_owner_preflight_html(preflight,csrf_token=ui4_csrf,ran=ran))
            except (ui4.UI4Error,ui1.UI1Error,ui2.UI2Error,p704.P704Error,OSError,ValueError):
                ui4.write_html(self,HTTPStatus.SERVICE_UNAVAILABLE,ui2._blocked_html("Owner preflight is unavailable."))
        def do_GET(self):
            parsed=urlsplit(self.path)
            if parsed.path==UNLOCK:
                if parsed.query: return self._unlock(HTTPStatus.BAD_REQUEST)
                try: ui2._require_loopback_host(self)
                except ui2.UI2BoundaryError: return self._unlock(HTTPStatus.BAD_REQUEST)
                return self._unlock()
            if parsed.path==ui4.PREFLIGHT_PATH:
                if parsed.query: return self._unlock(HTTPStatus.BAD_REQUEST)
                if self._gate(): return self._ui4()
                return
            if self._gate(): super().do_GET()
        def do_HEAD(self):
            parsed=urlsplit(self.path)
            if parsed.path==UNLOCK:
                if parsed.query: return self._unlock(HTTPStatus.BAD_REQUEST,body=False)
                try: ui2._require_loopback_host(self)
                except ui2.UI2BoundaryError: return self._unlock(HTTPStatus.BAD_REQUEST,body=False)
                return self._unlock(body=False)
            if parsed.path==ui4.PREFLIGHT_PATH:
                if parsed.query: return self._unlock(HTTPStatus.BAD_REQUEST,body=False)
                if self._gate(False): return self._ui4()
                return
            if self._gate(False): super().do_HEAD()
        def do_POST(self):
            parsed=urlsplit(self.path)
            if parsed.path==UNLOCK:
                try: ui2._require_same_origin(self); fields=_form(self)
                except (ui2.UI2BoundaryError,UI3BoundaryError): return self._unlock(HTTPStatus.BAD_REQUEST)
                if not hmac.compare_digest(fields["csrf"],csrf) or not hmac.compare_digest(fields["access_secret"],ingress): return self._unlock(HTTPStatus.UNAUTHORIZED,True)
                self.send_response(HTTPStatus.SEE_OTHER.value); ui2._security_headers(self); self.send_header("Set-Cookie",f"{COOKIE}={session}; HttpOnly; SameSite=Strict; Path=/"); self.send_header("Location","/"); self.send_header("Content-Length","0"); self.end_headers(); return
            if parsed.path==ui4.RUN_PATH:
                if not self._gate(): return
                try:
                    ui2._require_same_origin(self); fields=ui4.read_run_form(self)
                    if not hmac.compare_digest(fields["csrf"],ui4_csrf): raise ui4.UI4BoundaryError("UI4 CSRF continuity mismatch")
                except (ui2.UI2BoundaryError,ui4.UI4BoundaryError):
                    return ui4.write_html(self,HTTPStatus.FORBIDDEN,ui2._blocked_html("Owner preflight is unavailable."))
                return self._ui4(ran=True)
            if self._gate(): super().do_POST()
        def do_PUT(self):
            if self._gate(): super().do_PUT()
        def do_PATCH(self):
            if self._gate(): super().do_PATCH()
        def do_DELETE(self):
            if self._gate(): super().do_DELETE()
    server.RequestHandlerClass=Handler; server.ui3_release_sha=rel; server.ui3_session_resets_on_restart=True; server.ui4_preflight_only=True
    return server

def parser()->argparse.ArgumentParser:
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest="command",required=True)
    i=s.add_parser("init"); i.add_argument("--runtime-root",required=True); i.add_argument("--host",default=HOST); i.add_argument("--port",type=int,default=PORT); i.add_argument("--credential-id"); i.add_argument("--json",action="store_true")
    v=s.add_parser("verify"); v.add_argument("--runtime-root",required=True); v.add_argument("--exact-release",action="store_true"); v.add_argument("--json",action="store_true")
    for name in ("serve","rotate-secret","remove-private-material"):
        q=s.add_parser(name); q.add_argument("--runtime-root",required=True)
    return p

def main(argv=None)->int:
    a=parser().parse_args(argv); root=Path(a.runtime_root)
    try:
        if a.command=="init":
            selected=a.credential_id
            if selected is None and _config(root).exists(): selected=load_config(root).credential_id
            access=resolve_operator_access(root,selected); value=initialize_private_access(root,host=a.host,port=a.port,credential_id=access.credential_id); value.update(inspect_grant_id=access.inspect_grant_id,interaction_grant_id=access.interaction_grant_id)
        elif a.command=="verify": value=verify_private_access(root,exact=a.exact_release)
        elif a.command=="rotate-secret": value=rotate_access_secret(root)
        elif a.command=="remove-private-material": remove_private_material(root); print("P7.06-UI3 private material removed"); return 0
        else:
            server=make_private_server(root)
            try: server.serve_forever(poll_interval=.5)
            finally: server.server_close()
            return 0
    except (UI3Error,ui4.UI4Error,p704.P704Error,p706.P706Error,ui1.UI1Error,ui2.UI2Error) as exc:
        print("P7.06-UI3 unavailable" if a.command=="serve" else f"P7.06-UI3 FAIL: {exc}",file=os.sys.stderr); return 1
    print(json.dumps(value,ensure_ascii=False,sort_keys=True) if getattr(a,"json",False) else "P7.06-UI3 PASS"); return 0

if __name__=="__main__": raise SystemExit(main())
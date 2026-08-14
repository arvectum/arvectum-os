# Arvectum Engineering Standard

**Document ID:** AES-001
**Version:** 0.1.0
**Status:** Bootstrap
**Scope:** Arvectum Engineering
**Applies to:** Arvectum OS, Tender Agent, Marketing Agent, Proxy Launcher, Discount Parser

## 1. Purpose

Arvectum Engineering Standard устанавливает единые правила разработки, тестирования, документирования, выпуска и сопровождения программных продуктов Арвектум.

Стандарт определяет процесс разработки, но не требует унификации внутренней архитектуры продуктов.

Arvectum OS является reference implementation инженерных практик, но продуктовые проекты не обязаны копировать его архитектуру.

## 2. Project model

Проекты делятся на следующие типы:

- **Platform** — инфраструктурные и платформенные компоненты.
- **Product** — самостоятельные пользовательские продукты.
- **Consumer** — продукты, использующие возможности платформы.
- **Tooling** — внутренние инструменты разработки и эксплуатации.

Текущая классификация:

- Arvectum OS — `platform`;
- Tender Agent — `product / consumer`;
- Marketing Agent — `product / consumer`;
- Proxy Launcher — `product`;
- Discount Parser — `product`.

Продуктовая логика consumer-проектов не должна переноситься в Arvectum OS только ради унификации.

## 3. Sources of truth

Для каждого проекта должен существовать однозначно определённый canonical repository.

Иерархия доверия:

1. canonical repository;
2. принятые RFC/ADR/policies;
3. состояние canonical branch;
4. CI evidence;
5. release artifacts;
6. рабочие обсуждения, ChatGPT, OpenCode и локальные заметки.

Решение, существующее только в чате, не считается canonical decision.

Локальная версия файла не считается канонической, пока она не синхронизирована с canonical repository.

## 4. Standard development lifecycle

Любое существенное изменение проходит цепочку:

ROADMAP → ACTION → IMPLEMENTATION → TEST → QA/PREFLIGHT → CANONICAL CLOSURE → NEXT ACTION

Пропуск этапов должен быть явно обоснован.

Разработка не должна переходить к следующему roadmap action, если предыдущее действие находится в неопределённом состоянии.

## 5. Action states

Разрешённые состояния:

- OPEN;
- IN PROGRESS;
- BLOCKED;
- DONE 100%.

Формулировки «почти готово», «вроде работает», «осталось немного» не заменяют формальный статус.

Для BLOCKED обязательно фиксируются:

- причина;
- внешний или внутренний blocker;
- что уже выполнено;
- условие разблокировки;
- работа, которую можно выполнять параллельно.

## 6. Definition of Done

Action получает статус DONE 100%, когда выполнены все применимые условия:

1. реализация завершена;
2. необходимые тесты добавлены или актуализированы;
3. обязательные тесты проходят;
4. обязательные CI checks проходят;
5. документация соответствует фактической реализации;
6. отсутствуют случайные staged/untracked изменения;
7. изменения находятся в canonical repository;
8. изменения интегрированы в canonical branch либо иным явно определённым canonical способом;
9. сохранены необходимые evidence;
10. roadmap/status обновлены;
11. указан следующий roadmap action.

Если хотя бы одно обязательное условие не выполнено, действие не должно называться DONE 100%.

## 7. QA maturity levels

Arvectum Engineering использует общую шкалу зрелости проверки.

### L1 — Static Validation

Примеры:

- syntax;
- lint;
- type checks;
- schema validation;
- compile checks;
- configuration validation.

### L2 — Unit / Component Validation

Изолированная проверка компонентов и бизнес-логики.

### L3 — Integration Validation

Проверка взаимодействия внутренних компонентов, БД, API, migration paths, networking abstractions и аналогичных систем.

### L4 — Repository / CI / Release Candidate Validation

Проверка состояния canonical repository и воспроизводимой сборки:

- CI;
- packaging;
- release candidate;
- dependency consistency;
- repository contracts;
- migration smoke;
- artifact verification.

### L5 — Owner-Operated Real Environment Preflight

Проверка владельцем проекта на реальной целевой машине или инфраструктуре.

Примеры:

- Mac mini;
- MacBook;
- Windows workstation;
- реальная локальная сеть;
- реальные OS permissions.

L5 не должен подменяться контейнером или mock environment, если проверяется поведение ОС.

### L6 — Controlled External Integration

Проверка с реальными внешними интеграциями в контролируемой среде.

Примеры:

- Telegram test channel;
- реальные API;
- ЕИС;
- design partner sandbox;
- клиентская тестовая машина.

### L7 — Pilot

Ограниченная эксплуатация реальными пользователями или реальным внутренним процессом.

### L8 — Production Readiness

Формальная готовность к production:

- operational documentation;
- rollback;
- observability;
- backup/recovery;
- security checks;
- release procedure;
- support procedure.

### L9 — Production

Фактическая production-эксплуатация с эксплуатационным контролем.

Не каждый проект обязан использовать все уровни, но значения уровней не должны переопределяться между проектами.

## 8. Project-specific quality extensions

Проект может добавлять проверки поверх Engineering Standard.

Примеры:

Arvectum OS:
- Constitution compliance;
- RFC/ADR validation;
- platform contracts;
- operator context;
- real-node preflight.

Discount Parser:
- pytest;
- Alembic upgrade/downgrade smoke;
- doctor/preflight;
- Telegram validation;
- packaged application smoke.

Proxy Launcher:
- OS-specific proxy tests;
- exact rollback validation;
- environment restoration;
- installer/portable artifact checks.

Project-specific requirements расширяют глобальный стандарт, но не ослабляют его без явно принятого решения.

## 9. Git rules

Для каждого проекта определяется один canonical default branch.

Предпочтительное имя:

main

Перед началом изменений необходимо установить:

- repository;
- current branch;
- HEAD;
- canonical branch;
- working-tree state;
- remotes.

Изменения выполняются в feature/hotfix branch, если проект не имеет явно задокументированного другого режима.

Рекомендуемые prefixes:

- feat/;
- fix/;
- hotfix/;
- docs/;
- ci/;
- eng/;
- release/.

Прямые изменения canonical branch допустимы только когда это явно разрешено project policy и риск изменения минимален.

## 10. Canonical closure

Закрытие action должно фиксировать как минимум:

- repository;
- branch;
- final commit SHA;
- canonical branch;
- test result;
- CI result;
- working-tree status;
- созданный release/tag/artifact, если применимо;
- итоговый статус;
- следующий roadmap action.

Если изменение существует только локально, canonical closure не достигнут.

## 11. Roadmap rules

Каждый активный проект должен иметь canonical roadmap.

Roadmap состоит из:

MILESTONE → ACTION → ACCEPTANCE CRITERIA

Action должен быть достаточно мал, чтобы можно было однозначно определить его завершённость.

Roadmap не должен превращаться в журнал работы. Выполненные действия могут сохраняться, но текущее состояние должно легко читаться.

Для каждого проекта всегда должен быть определён один основной NEXT ACTION.

Допускаются параллельные задачи при наличии blocker, но это должно быть явно отражено.

## 12. Development conversation protocol

Для каждого крупного проекта рекомендуется три типа рабочих контекстов.

CONTROL / ROADMAP

Используется для:

- roadmap;
- milestones;
- state;
- blockers;
- dependencies;
- приоритетов;
- canonical decisions.

В этом контексте не выполняется длительная низкоуровневая отладка.

DEVELOPMENT

Используется для последовательной реализации roadmap actions.

По завершении action обязательно фиксируется:

ACTION — DONE 100%

и:

NEXT ROADMAP ACTION — ...

RELEASE / INCIDENT

Используется для:

- release;
- packaging;
- hotfix;
- customer feedback;
- L4–L7;
- реальных машин;
- production incidents.

Цель разделения — не создавать отдельный чат на каждую мелкую задачу, а предотвращать смешивание roadmap и многословных диагностических журналов.

## 13. ChatGPT / OpenCode roles

ChatGPT и OpenCode являются engineering tools, но не источниками canonical truth.

ChatGPT — предпочтительные задачи:

- roadmap;
- архитектурный анализ;
- repository audit;
- review;
- CI analysis;
- документация;
- release coordination;
- connected GitHub operations;
- cross-project coordination.

OpenCode — предпочтительные задачи:

- локальные изменения файлов;
- кодирование;
- запуск локальных тестов;
- platform-specific операции;
- операции с реальной файловой системой;
- действия, требующие local OS access.

Для задач, передаваемых OpenCode, техническое задание должно включать:

- цель;
- repository/path;
- исходное состояние;
- scope;
- запреты;
- acceptance criteria;
- обязательные тесты;
- формат финального отчёта.

OpenCode не должен самостоятельно расширять scope без необходимости.

## 14. Documentation baseline

Проект должен постепенно прийти к наличию следующих логических документов:

- PROJECT;
- ROADMAP;
- ARCHITECTURE;
- DEVELOPMENT;
- TESTING;
- RELEASE;
- STATUS.

Физические имена и расположение могут отличаться в существующих проектах.

Нельзя проводить массовый рефакторинг структуры только ради соответствия именам файлов.

Сначала вводится governance, затем структура нормализуется при естественных изменениях.

## 15. Existing projects / no-bureaucracy rule

Внедрение стандарта в существующий проект не должно ломать работающий продукт.

Запрещено:

- менять архитектуру исключительно ради единообразия;
- переносить каталоги без практической необходимости;
- переписывать стабильный CI только потому, что он выглядит иначе;
- создавать документацию, не дающую операционной пользы;
- добавлять approval gates, которые не снижают реальный риск.

Стандарт должен уменьшать неопределённость, а не увеличивать административную нагрузку.

## 16. Repository audit requirement

Перед миграцией существующего проекта под стандарт проводится baseline audit.

Audit проверяет:

- repository identity;
- default branch;
- remotes;
- canonical HEAD;
- branches/tags;
- CI;
- tests;
- documentation;
- releases;
- build process;
- working-tree/local-only risks;
- secrets/security baseline;
- текущий roadmap;
- текущий QA level.

По результатам формируется gap list.

## 17. Mac mini workspace rule

Перестройка локальных рабочих каталогов допустима только после:

1. инвентаризации всех активных репозиториев;
2. проверки их canonical remote state;
3. выявления локальных-only изменений;
4. резервного сохранения значимых данных;
5. определения canonical local paths.

Изменение путей не должно происходить до завершения этих проверок.

## 18. Arvectum OS pilot gate

Pilot Arvectum OS на Mac mini начинается только после:

1. закрытия требуемого L4 для текущего release candidate;
2. подтверждения canonical repository state;
3. успешного owner-operated L5 preflight;
4. проверки rollback/recovery procedure;
5. подготовки runtime workspace.

После этого Mac mini может рассматриваться как первый реальный Arvectum Node.

## 19. Governance inheritance

Корпоративная модель:

Arvectum Engineering Standard → Project Policy → RFC/ADR → Implementation

Project policy не должна молча противоречить глобальному стандарту.

Осознанное исключение фиксируется отдельным решением с причиной.

## 20. Versioning

Engineering Standard использует Semantic Versioning по смыслу:

- PATCH — уточнение без изменения требований;
- MINOR — новое обратно совместимое правило;
- MAJOR — несовместимое изменение обязательного engineering process.

Версия 0.x считается bootstrap-периодом.

## 21. Bootstrap canonical location

До создания отдельного corporate governance repository временным canonical bootstrap location является:

arvectum/arvectum-os/docs/governance/ARVECTUM-ENGINEERING-STANDARD.md

Это расположение не означает, что Arvectum Engineering Standard является частью архитектуры Arvectum OS.

После появления отдельного governance repository документ должен быть перенесён туда, а Arvectum OS должен ссылаться на корпоративный источник.

## 22. Initial adoption order

Стандарт внедряется волнами:

1. Arvectum Engineering governance;
2. Arvectum OS как reference implementation;
3. Proxy Launcher и Discount Parser;
4. Tender Agent;
5. Marketing Agent;
6. Mac mini workspace normalization;
7. Arvectum OS L5 → pilot.

End of Arvectum Engineering Standard v0.1.0

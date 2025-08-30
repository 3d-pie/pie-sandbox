# Phase‑1 Challenges – 3D PIE Sandbox


## Overview – Two‑Phase Path

| Phase | Where it happens | Scope & Purpose |
| ----- | ---------------- | --------------- |
| **Phase 1** | **Sandbox repo** (this one) | Build small, isolated proofs of concept. Focus on core logic only – minimal UI, no infra coupling. Goal: validate your grasp of Flask, SQLAlchemy, file handling, and clean code without overwhelming context. |
| **Phase 2** | **Main product repo** (unlocked after Phase 1 passes code review) | Take the working POCs and hard‑wire them into production: real migrations, polished admin UI, background workers, testing, CI. Goal: ship features that survive load and team workflows. |

*Why split it?*  A confined sandbox lets you iterate fast and show mastery without risking the main code‑base. Once you clear Phase 1, you’ll already have a mental model and can focus on integration details instead of starting from scratch.

---

## Prerequisites

Python 3.11 – download it [here](https://www.python.org/downloads/)



## Why these challenges?

| Challenge | Purpose |
| --------- | ------- |
| **RBAC** | Retire brittle boolean flags and move to fine‑grained, scalable permissions. We’ll need this for multi‑tenant and delegated admin features down the road. |
| **G‑Code Insight** | Print time & material cost are mission‑critical for quoting, scheduling, and sustainability metrics. A performant parser demonstrates your ability to optimise I/O heavy tasks. |
| **Thumbnail Renderer** | Visual feedback speeds up workflow decisions and reduces operator error. Generating previews without blocking the request path shows you understand async patterns and user experience. |

---

This file describes what you need to **implement** inside the sandbox repository.  The repo already ships with minimal stubs (see separate scaffold docs).  Your job is to flesh them out and meet the acceptance criteria.

> **Legend**\
> **SR** – Feature stub that is already provided in the scaffold so you can start coding immediately.

---

## Challenge 1 · Role‑Based Access Control (RBAC)

### Phase 1 tasks

1. **Schema migration** – Replace legacy boolean flags `is_admin`, `is_primary_admin` with `Role`, `Permission`, `UserRole` tables (many‑to‑many).  Provide an Alembic migration that converts data in place.
2. **RBAC API** – Add `current_user.has_perm("foo")` helper.
3. **Role demo** – `/rbac/demo` route prints current user’s roles & permissions.
4. **Role variety** – Create at least two roles with distinct permission sets (e.g., `operator`, `manager`).


**Tip: Inspect the SQLite database quickly with [DB Browser for SQLite](https://sqlitebrowser.org/).**

**SR**

- The scaffold already contains a `/login` page powered by Flask‑Login.
- Highest role (`superadmin`) can edit other users’ roles via `/admin/roles` stub UI.


**Done when**

- Migration runs on the sample DB without data loss.
- Demo route shows two roles after you create them via a tiny script or UI.

### Phase 2 tasks

- Replace all hard‑coded flag checks with `has_perm`.
- Extend admin UI so new roles are usable instantly.

---

## Challenge 2 · G‑Code Insight Extractor

### Phase 1 tasks

1. **Parser implementation** – Complete `gcode_parser(path)` (Python 3.11 *or* C++ via pybind11/CLI) to output JSON:

   ```json
   {
     "filament_mm": 1234.0,
     "filament_g": 15.3,
     "estimated_minutes": 42
   }
   ```

   Must finish ≤ 1 s on a 10 MB file.

2. **Upload workflow** – `/gcode/upload` form lets users choose a `.gcode` file. On submit, call the parser and **return the JSON** to the browser.


**SR**

- Upload form template and route stub already exist; parser function currently `pass`.

**Done when**

- Sample G‑Code returns correct stats.
- Upload route responds 200 with JSON body.

### Phase 2 tasks

- Automatically parse stats when admin uploads a G‑Code for an item; persist into `Item.meta`.

---

## Challenge 3 · Thumbnail Renderer

### Phase 1 tasks

1. **Thumbnail generation** – Finish `thumbnail_render(path)` to create a ≤ 512×512 PNG from an STL/3MF model using `trimesh` + `Pillow`. Save PNG under `/uploads` and return relative path.


2. **Upload + DB** – Route `/thumbs/upload` accepts model file, saves it, creates a new `Item` row, stores the thumbnail path in `Item.meta["thumb"]`, and finally renders `items_list.html` with all items.

**SR**

- Upload route and `thumbnail_render` stub already wired in scaffold.
- `items_list.html` template lists items and shows thumbnail if `meta.thumb` is set.

**Done when**

- Uploading a model returns **201** or redirect, item appears on list, and PNG opens.

### Phase 2 tasks

- Hook thumbnail creation into general upload flow; keep request ≤ 200 ms (consider threading).

---

## Git basics & submission

You’ll be working in a public GitHub repo that already contains the sandbox scaffold. **One branch for all Phase‑1 work is perfectly fine**—feel free to split things up if you prefer, but it’s not required.

```bash
# 1. Fork (or clone if you already have rights) and get the code
$ git clone https://github.com/3d-pie/pie-sandbox.git
$ cd 3d‑pie‑sandbox

# 2. Create (or check out) a single working branch
$ git checkout -b phase1

# 3. Build, code, commit – early and often
$ docker compose up  # make sure it boots
$ git add app/models.py migrations/0001_rbac.py
$ git commit -m "feat: rbac migration skeleton"

# 4. Push and open a Pull Request back to the upstream sandbox repo
$ git push -u origin phase1
```

Keep pushing commits as you iterate When:

1.  `docker compose up` starts without errors

…request a review. We’ll merge once everything looks solid. That unlocks access to the main repo for Phase 2.

> **Open brief on purpose:** The instructions stay deliberately broad so you can explore Flask, SQLAlchemy, and clean architecture in your own style. Rename modules, add linters, tests—just keep `docker compose up` green.


# Smart Electricity Billing System

## Frontend Upgrade Guide (Tailwind SaaS UI)

This guide documents how the project was upgraded from a basic dashboard to a modern shadcn-inspired SaaS interface using Django templates.

The visual direction is based on the reference style you shared:

- clean sidebar + top navbar layout
- rounded cards with soft borders/shadows
- muted grayscale base with brand accents
- compact analytics panels
- premium but simple typography

---

## 1. Tailwind Setup

Node tooling was added in the existing Django project (without changing backend architecture).

```bash
npm init -y
npm install -D tailwindcss@3.4.13 postcss@8.4.49 autoprefixer@10.4.20
npx tailwindcss init -p
```

Build command:

```bash
npm run build:css
```

Watch mode:

```bash
npm run watch:css
```

---

## 2. Tailwind Configuration

Configured files:

- `tailwind.config.js`
- `postcss.config.js`
- `static/src/input.css`
- `static/css/output.css` (generated)

Template scanning paths used:

- `templates/**/*.html`
- `billing/**/*.py`
- `static/js/**/*.js`

Dark mode:

- class-based (`darkMode: "class"`)
- toggled with `localStorage` in browser

---

## 3. Base Layout

Main layout file:

- `templates/base.html`

What was changed:

- removed Bootstrap assets
- added Tailwind compiled CSS
- added Manrope font
- added Alpine.js, Chart.js, and Lucide script includes
- implemented authenticated app shell and auth-only rendering
- added dark mode initialization script

---

## 4. Reusable Partials

Created:

- `templates/partials/sidebar.html`
- `templates/partials/navbar.html`

Sidebar includes:

- logo/brand area
- route-aware active states
- mobile slide-in behavior
- system status block

Navbar includes:

- mobile sidebar toggle
- theme toggle
- username pill
- logout action

---

## 5. Reusable Components

Created under `templates/components/`:

- `card.html`
- `stats-card.html`
- `table.html`
- `badge.html`
- `modal.html`

Used actively:

- `stats-card.html` on dashboard KPI grid
- `badge.html` for Paid/Pending status labels

---

## 6. Dashboard UI Upgrade

File:

- `templates/dashboard.html`

Implemented:

- 5 analytics cards:
  - Total Consumers
  - Total Bills
  - Paid Bills
  - Pending Bills
  - Monthly Revenue
- Monthly usage bar chart
- Revenue trend line chart
- Paid vs Pending doughnut chart
- recent bills table
- quick action panel

Chart data is passed from Django view (`billing/views.py`) as JSON.

---

## 7. Consumer Management UI

Files:

- `templates/consumer_list.html`
- `templates/consumer_form.html`
- `templates/consumer_detail.html`

Implemented:

- searchable consumer list
- responsive data table
- row action dropdown (view/edit/delete)
- polished add/edit form in card layout
- consumer profile summary with bill history

Backend enhancement:

- search query now uses `Q(...)` filter with `.distinct()`

---

## 8. Bill Generation UI

File:

- `templates/generate_bill.html`

Implemented:

- modern billing form card
- tariff summary side card
- live amount preview card:
  - units used
  - energy charge
  - tax
  - total amount

Live preview logic in:

- `static/js/main.js`

---

## 9. Bill History + Pagination UI

File:

- `templates/bill_list.html`

Implemented:

- status filters (All/Paid/Pending)
- modern table and action buttons
- pagination controls

Backend enhancement:

- `Paginator` added in `billing/views.py` (`10` rows per page)

---

## 10. Bill Detail / Invoice UI

File:

- `templates/bill_detail.html`

Implemented:

- invoice header with status
- consumer and reading summary
- amount breakdown section
- print button
- download PDF button
- mark paid button (for pending bills)

---

## 11. Static Assets Setup

Frontend assets:

- `static/src/input.css` (Tailwind source)
- `static/css/output.css` (compiled CSS)
- `static/js/main.js` (charts, dark mode, lucide icons, bill preview)

Do not edit `output.css` manually. Rebuild it after class changes:

```bash
npm run build:css
```

---

## 12. Final Folder Structure

```text
electricitybillmanagementsystem/
├── billing/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── docs/
│   ├── DATABASE_GUIDE.md
│   └── FRONTEND_UPGRADE_GUIDE.md
├── static/
│   ├── css/
│   │   └── output.css
│   ├── js/
│   │   └── main.js
│   └── src/
│       └── input.css
├── templates/
│   ├── components/
│   │   ├── badge.html
│   │   ├── card.html
│   │   ├── modal.html
│   │   ├── stats-card.html
│   │   └── table.html
│   ├── partials/
│   │   ├── navbar.html
│   │   └── sidebar.html
│   ├── registration/
│   │   └── login.html
│   ├── base.html
│   ├── dashboard.html
│   ├── consumer_list.html
│   ├── consumer_form.html
│   ├── consumer_detail.html
│   ├── bill_list.html
│   ├── generate_bill.html
│   ├── bill_detail.html
│   └── confirm_delete.html
├── package.json
├── postcss.config.js
├── tailwind.config.js
└── manage.py
```

---

## 13. Run Instructions

Backend:

```bash
source venv/bin/activate
python manage.py runserver
```

Frontend CSS build:

```bash
npm run build:css
```

Optional continuous development:

```bash
npm run watch:css
```

---

## 14. Viva/Demo Talking Points

Use this short explanation in viva:

1. Backend is Django with function-based views and SQLite.
2. Frontend is server-rendered Django templates with Tailwind CSS.
3. UI is componentized using reusable `partials` and `components`.
4. Chart.js provides analytics visualization for usage/revenue/status.
5. Bill amounts are auto-calculated using slab tariff logic.
6. ReportLab generates downloadable electricity bill PDFs.
7. Consumers also have a dedicated portal login (`/consumer/login/`) to view their own bills and status.

This makes the project easy to explain, easy to run, and visually strong for demo/portfolio.

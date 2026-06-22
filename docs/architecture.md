# Architecture

The framework is organised in four independent test layers driven by a shared
configuration and a common set of pytest markers. A traceability generator sits
on top, reading the `@pytest.mark.req(...)` markers off the live suite to keep
the requirements matrix honest.

```mermaid
flowchart TB
    subgraph CFG[Configuration]
        ENV[".env / env vars"] --> SET["config/settings.py<br/>(pydantic-settings)"]
    end

    subgraph SRC["src/ (tested support library)"]
        PC[price_calculator]
        SV[schema_validator]
        DB[data_builders]
    end

    subgraph TESTS[Test layers]
        UNIT["unit/<br/>pytest + coverage"]
        API["api/<br/>httpx -> restful-booker"]
        UI["ui/<br/>Playwright POM -> SauceDemo"]
        BDD["bdd/<br/>Gherkin + pytest-bdd"]
    end

    subgraph POM["Page Object Model"]
        LP[LoginPage] --> IP[InventoryPage] --> CART[CartPage] --> CO[CheckoutPage]
    end

    SET --> API
    SET --> UI
    SET --> BDD
    SRC --> UNIT
    SV --> API
    DB --> API
    PC --> UI
    POM --> UI
    POM --> BDD

    TESTS --> MARK["@pytest.mark.req(...)"]
    MARK --> TRACE["scripts/gen_traceability.py"]
    REG["docs/requirements.json"] --> TRACE
    TRACE --> MATRIX["traceability_matrix.md / .csv"]

    TESTS --> REPORTS["reports/<br/>pytest-html + Allure + traces"]

    subgraph CI["GitHub Actions (parallel jobs)"]
        L[lint] & U[unit] & A[api] & UX[ui x3 browsers] & B[bdd] & T[traceability] & P[perf k6]
    end

    TESTS --> CI
    TRACE --> CI
```

## Design choices

| Concern | Decision | Why |
|---|---|---|
| UI target | SauceDemo | Stable, designed for automation, clean e-commerce flow for requirement mapping. |
| API target | restful-booker | Full CRUD + token auth + a real booking domain (stateful workflow). |
| Config | pydantic-settings, env-driven, safe defaults | Runs out of the box; overridable per environment without code changes. |
| Coverage meaning | unit tests target `src/`, reused by UI assertions | Coverage measures real logic, not throwaway code. |
| Traceability | generated from live markers, CI-verified | Cannot silently drift — mirrors critical-systems QA practice. |
| Flakiness | Playwright auto-wait, reruns, Heroku wake-up ping, failure artifacts | Robust against external demo-service variability. |

from utilities.pydantic_models import demo as pydantic_demo
from utilities.query_validation_transformation import handle_query
from utilities.logging_example import run_logging_demo
from utilities.mem0_example import run_observability_demo


def main():
    print("=" * 60)
    print("PHASE 1: Pydantic Models Demo")
    print("=" * 60)
    pydantic_demo()

    print("
" + "=" * 60)
    print("PHASE 2: Query Validation & Transformation")
    print("=" * 60)
    result = handle_query("Find the latest AI trends and buy some books")
    for k, v in result.items():
        print(f"  {k:12}: {v}")

    print("
" + "=" * 60)
    print("PHASE 3: Logging Demo")
    print("=" * 60)
    run_logging_demo()

    print("
" + "=" * 60)
    print("PHASE 4: Mem0 Observability Demo")
    print("=" * 60)
    run_observability_demo()


if __name__ == "__main__":
    main()
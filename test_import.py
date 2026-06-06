
import sys

errors = []


def check_import(package_name, import_name=None):
    name = import_name or package_name
    try:
        __import__(name)
        print(f"  ✅ {package_name}")
    except ImportError as e:
        print(f"  ❌ {package_name} — NOT installed ({e})")
        errors.append(package_name)


print("=" * 50)
print("  Checking installed packages...")
print("=" * 50)

check_import("langchain")
check_import("langchain-groq", "langchain_groq")
check_import("langchain-community", "langchain_community")
check_import("groq")
check_import("wikipedia")
check_import("duckduckgo-search", "duckduckgo_search")
check_import("python-dotenv", "dotenv")

print()
if errors:
    print(f"❌ Missing packages: {', '.join(errors)}")
    print(f"   Fix with: pip install {' '.join(errors)}")
else:
    print("✅ All packages installed! Run: python test/test_groq.py")

print("=" * 50)

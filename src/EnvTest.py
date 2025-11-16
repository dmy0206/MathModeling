import sys
print("=== 当前Python环境 ===")
print("Python路径:", sys.executable)
print("Python版本:", sys.version)

print("\n=== 包安装位置 ===")
print("site-packages路径:", [p for p in sys.path if 'site-packages' in p])

print("\n=== numpy检查 ===")
try:
    import numpy
    print("✅ numpy版本:", numpy.__version__)
    print("numpy路径:", numpy.__file__)
except ImportError:
    print("❌ numpy未安装")
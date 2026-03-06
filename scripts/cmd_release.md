## 方法1: 手动发布（PowerShell）

### 1. 打包
```bash
Remove-Item build, dist -Recurse -Force -ErrorAction SilentlyContinue

python -m build

python -m twine check dist/*

```

### 2. 上传至pypi
```bash

python -m twine upload dist/*

```
### 3. 上传至testpypip
```bash

python -m twine upload --repository testpypi dist/*

```
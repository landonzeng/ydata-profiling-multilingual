def diagnose_font_issues():
    """诊断字体配置问题 - 增强版"""
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    import platform
    from pathlib import Path

    print("=" * 60)
    print("字体配置诊断报告 (增强版)")
    print("=" * 60)

    # 1. 系统信息
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"Python版本: {platform.python_version()}")

    # 2. 检查ydata-profiling内置字体
    print(f"\n🔍 检查ydata-profiling内置字体:")
    builtin_font_paths = [
        "src/ydata_profiling/assets/fonts/simhei.ttf"
    ]

    builtin_font_found = None
    for font_path in builtin_font_paths:
        if Path(font_path).exists():
            builtin_font_found = font_path
            print(f"  ✅ 找到内置字体: {font_path}")

            # 获取字体文件详细信息
            font_size = Path(font_path).stat().st_size
            print(f"     文件大小: {font_size:,} bytes")

            # 尝试加载字体属性
            try:
                prop = fm.FontProperties(fname=font_path)
                font_name = prop.get_name()
                print(f"     字体名称: {font_name}")
            except Exception as e:
                print(f"     ❌ 字体文件损坏: {e}")
            break

    if not builtin_font_found:
        print("  ❌ 未找到内置字体文件")
        print("     请确认simhei.ttf文件存在于ydata_profiling/assets/fonts/目录中")

    # 3. 检查字体管理器中已注册的字体
    print(f"\n🔍 检查matplotlib已注册的字体:")
    registered_chinese_fonts = []

    for font in fm.fontManager.ttflist:
        font_path = getattr(font, 'fname', '')
        font_name = getattr(font, 'name', '')

        # 检查是否是中文字体或我们添加的字体
        is_chinese_font = any(keyword in font_name.lower() for keyword in
                              ['simhei', 'yahei', 'simsun', 'pingfang', 'heiti', 'wenquanyi', 'noto'])

        is_builtin_font = 'ydata_profiling' in font_path or 'simhei' in font_path.lower()

        if is_chinese_font or is_builtin_font:
            registered_chinese_fonts.append({
                'name': font_name,
                'path': font_path,
                'is_builtin': is_builtin_font
            })

    if registered_chinese_fonts:
        for font_info in registered_chinese_fonts[:10]:  # 显示前10个
            builtin_mark = "🏠" if font_info['is_builtin'] else "🖥️"
            print(f"  {builtin_mark} {font_info['name']}")
            print(f"     路径: {font_info['path']}")
    else:
        print("  ❌ matplotlib中未找到已注册的中文字体")

    # 4. 当前matplotlib字体配置
    print(f"\n🔍 当前matplotlib字体配置:")
    current_fonts = plt.rcParams['font.sans-serif']
    print(f"  font.sans-serif: {current_fonts[:5]}")  # 显示前5个
    print(f"  font.family: {plt.rcParams['font.family']}")
    print(f"  axes.unicode_minus: {plt.rcParams['axes.unicode_minus']}")

    # 5. 测试字体解析
    print(f"\n🔍 测试字体解析:")
    test_fonts = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']

    for font_name in test_fonts:
        try:
            font_prop = fm.FontProperties(family=font_name)
            actual_font_path = fm.findfont(font_prop)

            # 检查是否解析到了我们期望的字体
            if font_name == 'SimHei' and builtin_font_found:
                expected_path = Path(builtin_font_found).resolve()
                actual_path = Path(actual_font_path).resolve()

                if expected_path == actual_path:
                    print(f"  ✅ {font_name}: 正确解析到内置字体")
                    print(f"     {actual_font_path}")
                else:
                    print(f"  ⚠️ {font_name}: 解析到其他字体")
                    print(f"     期望: {expected_path}")
                    print(f"     实际: {actual_path}")
            else:
                print(f"  🔍 {font_name}: {actual_font_path}")

        except Exception as e:
            print(f"  ❌ {font_name}: 解析失败 - {e}")

    # 6. 检查setup_chinese_fonts是否被调用
    print(f"\n🔍 检查字体设置状态:")
    try:
        from ydata_profiling.assets.fonts.font_manager import get_font_manager
        font_manager = get_font_manager()
        font_info = font_manager.get_font_info()

        print(f"  字体管理器状态:")
        print(f"    已初始化: {font_info.get('font_initialized', False)}")
        print(f"    内置字体可用: {font_info.get('chinese_font_available', False)}")
        print(f"    内置字体列表: {font_info.get('bundled_fonts', [])}")
        print(f"    字体目录: {font_info.get('font_dir', 'Unknown')}")

    except ImportError:
        print("  ❌ 无法导入字体管理器模块")
    except Exception as e:
        print(f"  ❌ 获取字体管理器状态失败: {e}")

    return {
        'builtin_font_found': builtin_font_found,
        'registered_chinese_fonts': registered_chinese_fonts,
        'current_font_config': current_fonts
    }


def test_font_setup_sequence():
    """测试字体设置序列"""
    print("🧪 测试字体设置序列")
    print("=" * 40)

    # 1. 调用setup_chinese_fonts
    print("步骤1: 调用setup_chinese_fonts()")
    try:
        from ydata_profiling.assets.fonts.font_manager import setup_chinese_fonts
        result = setup_chinese_fonts(True)
        print(f"  返回结果: {result}")
    except Exception as e:
        print(f"  ❌ 调用失败: {e}")
        return False

    # 2. 诊断字体状态
    print("\n步骤2: 诊断字体状态")
    diagnosis = diagnose_font_issues()

    # 3. 生成测试图片
    print("\n步骤3: 生成测试图片")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.text(0.5, 0.7, '内置字体测试：一层门诊药房办公用电',
            ha='center', va='center', fontsize=16,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen"))

    ax.text(0.5, 0.3, f"当前字体: {plt.rcParams['font.sans-serif'][0]}",
            ha='center', va='center', fontsize=12)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title('字体设置序列测试', fontsize=18)
    ax.axis('off')

    try:
        plt.savefig('font_setup_sequence_test.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("  ✅ 测试图片已保存: font_setup_sequence_test.png")
    except Exception as e:
        print(f"  ❌ 保存失败: {e}")
        plt.close()

    return diagnosis


# 使用方法
if __name__ == "__main__":
    # 先调用setup_chinese_fonts
    print("🚀 开始字体设置测试")
    test_result = test_font_setup_sequence()

    # 分析结果
    if test_result and test_result.get('builtin_font_found'):
        print("\n✅ 成功找到并配置了内置字体！")
    else:
        print("\n❌ 内置字体配置可能有问题")
"""
Complete workflow example for custom translations in ydata-profiling
演示如何使用 ydata-profiling 的自定义翻译功能的完整工作流程
"""
import warnings

import pandas as pd
import json
import shutil
from pathlib import Path

from matplotlib import pyplot as plt

from ydata_profiling import ProfileReport
from ydata_profiling.i18n import (
    export_translation_template,
    load_translation_file,
    add_translation_directory,
    set_locale,
    get_available_locales,
    get_locale,
    _
)


# 配置输出目录
OUTPUT_DIR = Path("output")


def setup_output_directory():
    """创建输出目录"""
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"📁 Output directory: {OUTPUT_DIR.absolute()}")
    return OUTPUT_DIR


def setup_chinese_fonts():
    """配置matplotlib支持中文字体"""
    # 抑制字体警告
    warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

    # 检查是否有本地字体文件
    font_files = [
        Path("/src/ydata_profiling/assets/fonts/simhei.ttf"),  # 本地字体目录
        # "SimHei",  # 系统字体名
        "Microsoft YaHei",  # 微软雅黑
        "PingFang SC",  # macOS
        "WenQuanYi Micro Hei",  # Linux
        "DejaVu Sans"  # 备用
    ]

    font_found = False
    for font in font_files:
        try:
            if isinstance(font, Path) and font.exists():
                # 注册本地字体文件
                from matplotlib.font_manager import fontManager
                fontManager.addfont(str(font))
                font_name = font.stem
                print(f"✅ 加载本地字体文件: {font}")
                font_found = True
                break
            elif isinstance(font, str):
                # 测试系统字体
                plt.rcParams['font.sans-serif'] = [font] + plt.rcParams['font.sans-serif']
                print(f"✅ 使用系统字体: {font}")
                font_found = True
                break
        except Exception as e:
            continue

    # 设置字体配置
    plt.rcParams['font.sans-serif'] = [
        'SimHei',  # 黑体
        'Microsoft YaHei',  # 微软雅黑
        'PingFang SC',  # 苹方 (macOS)
        'STHeiti',  # 华文黑体 (macOS)
        'WenQuanYi Micro Hei',  # 文泉驿微米黑 (Linux)
        'Noto Sans CJK SC',  # 思源黑体 (Linux)
        'DejaVu Sans',  # 备用西文字体
        'Arial'  # 最后备用
    ]
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    if font_found:
        print("✅ 中文字体配置完成")
    else:
        print("⚠️ 未找到理想的中文字体，使用系统默认字体")

    return font_found

def create_sample_data():
    """创建示例数据"""
    print("📊 Creating sample dataset...")

    df = pd.DataFrame({
        'bt': [
            '2025-10-10 10:05:00', '2025-10-10 10:10:00', '2025-10-10 10:15:00', '2025-10-10 10:20:00',
            '2025-10-10 10:25:00', '2025-10-10 10:30:00', '2025-10-10 10:35:00', '2025-10-10 10:40:00',
            '2025-10-10 10:45:00', '2025-10-10 10:50:00', '2025-10-10 10:55:00', '2025-10-10 11:00:00'
        ],
        '总用电量': [
            54033.6, 54033.6, 54033.6, 54033.6,
            54034.2, 54034.2, 54034.2, 54034.2,
            54034.8, 54034.8, 54035.4, 54035.4
        ],
        '冷机用电量': [
            300265.2, 300266.4, 300267.6, 300268.8,
            300270, 300271.2, 300272.4, 300273.6,
            300274.8, 300276.6, 300277.8, 300279.1
        ],
        '空调系统总用电量': [
            18101.43, 18101.43, 18101.43, 18101.43,
            18101.95, 18101.95, 18101.95, 18101.95,
            18101.95, 18101.95, 18101.95, 18101.95
        ]
    })

    df['bt'] = pd.to_datetime(df['bt'])

    print(f"✅ Sample dataset created with {len(df)} rows and {len(df.columns)} columns")
    print(f"📋 Columns: {', '.join(df.columns.tolist())}")
    return df


def step1_export_template():
    """步骤1: 导出翻译模板"""
    print("\n🔧 Step 1: Exporting translation template...")

    # 导出英文模板作为翻译基础到output目录
    template_file = OUTPUT_DIR / "en_translation_template.json"
    export_translation_template('en', template_file)

    print(f"✅ Translation template exported to: {template_file}")

    # 显示模板内容预览
    with open(template_file, 'r', encoding='utf-8') as f:
        template_data = json.load(f)

    print("📋 Template structure preview:")
    for section in template_data.keys():
        if isinstance(template_data[section], dict):
            print(f"  📁 {section}: {len(template_data[section])} keys")
            # 显示前几个子键
            sub_keys = list(template_data[section].keys())[:3]
            if sub_keys:
                print(f"    └── {', '.join(sub_keys)}...")
        else:
            print(f"  📄 {section}: {template_data[section]}")

    return template_file


def step2_create_custom_translations(template_file):
    """步骤2: 基于模板创建自定义翻译"""
    print(f"\n🌍 Step 2: Creating custom translations based on {template_file}...")

    # 读取模板
    with open(template_file, 'r', encoding='utf-8') as f:
        template = json.load(f)

    # 创建法语翻译（基于实际的翻译键结构）
    french_translation = {
        "report": {
            "overview": "Aperçu",
            "variables": "Variables",
            "interactions": "Interactions",
            "missing_values": "Valeurs manquantes",
            "sample": "Échantillon",
            "duplicates": "Lignes dupliquées",
            "footer_text": "Rapport généré par <a href=\"https://ydata.ai/?utm_source=opensource&utm_medium=pandasprofiling&utm_campaign=report\">YData</a>.",
            "most_frequently_occurring": "Le plus fréquent",
            "columns": "Colonnes",
            "more_details": "Plus de détails"
        },
        "rendering": {
            "generate_structure": "Générer la structure du rapport",
            "html_progress": "Rendu HTML",
            "json_progress": "Rendu JSON",
            "widgets_progress": "Rendu des widgets",
            "other_values_count": "Autres valeurs ({other_count})"
        },
        "core": {
            "unknown": "inconnu",
            "alerts": {
                "title": "Alertes",
                "alerts_high_correlation_tip": "Cette variable a une forte corrélation {corr} avec {num} champs : {title}",
                "correlation_types": {
                    "overall": "globale"
                }
            },
            "collapse": "Réduire",
            "container": "Conteneur",
            "correlationTable": "TableauDeCorrelation",
            "dropdown": "Menu déroulant",
            "duplicate": "Dupliquer",
            "html": "HTML",
            "image": "Image",
            "sample": "Échantillon",
            "scores": "Scores",
            "table": "Tableau",
            "toggle_button": "Bouton basculer",
            "variable": "Variable",
            "variable_info": "InfoVariable",
            "model": {
                "bar_count": "Nombre",
                "bar_caption": "Une visualisation simple de la nullité par colonne.",
                "matrix": "Matrice",
                "matrix_caption": "La matrice de nullité est un affichage dense de données qui vous permet de repérer rapidement visuellement les modèles dans la complétude des données.",
                "heatmap": "Carte de chaleur",
                "heatmap_caption": "La carte de chaleur de corrélation mesure la corrélation de nullité : à quel point la présence ou l'absence d'une variable affecte la présence d'une autre.",
                "first_rows": "Premières lignes",
                "last_rows": "Dernières lignes",
                "random_sample": "Échantillon aléatoire"
            },
            "structure": {
                "correlations": "Corrélations",
                "heatmap": "Carte de chaleur",
                "table": "Tableau",
                "overview": {
                    "values": "valeurs",
                    "number_variables": "Nombre de variables",
                    "number_observations": "Nombre d'observations",
                    "number_of_series": "Nombre de séries",
                    "missing_cells": "Cellules manquantes",
                    "missing_cells_percentage": "Cellules manquantes (%)",
                    "duplicate_rows": "Lignes dupliquées",
                    "duplicate_rows_percentage": "Lignes dupliquées (%)",
                    "total_size_memory": "Taille totale en mémoire",
                    "average_record_memory": "Taille moyenne d'enregistrement en mémoire",
                    "dataset_statistics": "Statistiques du jeu de données",
                    "variable_types": "Types de variables",
                    "variable_descriptions": "Descriptions des variables",
                    "overview": "Aperçu",
                    "url": "URL",
                    "copyright": "Droits d'auteur",
                    "dataset": "Jeu de données",
                    "analysis_started": "Analyse commencée",
                    "analysis_finished": "Analyse terminée",
                    "duration": "Durée",
                    "software_version": "Version du logiciel",
                    "download_configuration": "Télécharger la configuration",
                    "reproduction": "Reproduction",
                    "variables": "Variables",
                    "alerts_count": "Alertes ({count})",
                    "timeseries_length": "Longueur des séries temporelles",
                    "starting_point": "Point de départ",
                    "ending_point": "Point de fin",
                    "period": "Période",
                    "timeseries_statistics": "Statistiques des séries temporelles",
                    "original": "Original",
                    "scaled": "Mis à l'échelle",
                    "time_series": "Séries temporelles",
                    "interactions": "Interactions",
                    "distinct": "Distinct",
                    "distinct_percentage": "Distinct (%)",
                    "missing": "Manquant",
                    "missing_percentage": "Manquant (%)",
                    "memory_size": "Taille mémoire",
                    "file": "Fichier",
                    "size": "Taille",
                    "file_size": "Taille du fichier",
                    "file_size_caption": "Histogramme avec des bacs de taille fixe des tailles de fichiers (en octets)",
                    "unique": "Unique",
                    "unique_help": "Le nombre de valeurs uniques (toutes les valeurs qui apparaissent exactement une fois dans le jeu de données).",
                    "unique_percentage": "Unique (%)",
                    "max_length": "Longueur max",
                    "median_length": "Longueur médiane",
                    "mean_length": "Longueur moyenne",
                    "min_length": "Longueur min",
                    "length": "Longueur",
                    "length_histogram": "histogramme de longueur",
                    "histogram_lengths_category": "Histogramme des longueurs de la catégorie",
                    "most_occurring_categories": "Catégories les plus fréquentes",
                    "frequency": "Frequency",
                    "most_frequent_character_per_category": "Caractère le plus fréquent par catégorie",
                    "most_occurring_scripts": "Scripts les plus fréquents",
                    "most_frequent_character_per_script": "Caractère le plus fréquent par script",
                    "most_occurring_blocks": "Blocs les plus fréquents",
                    "most_frequent_character_per_block": "Caractère le plus fréquent par bloc",
                    "imaginary": "Imaginary",
                    "real": "Real",
                    "total_characters": "Total des caractères",
                    "distinct_characters": "Caractères distincts",
                    "distinct_categories": "Catégories distinctes",
                    "unicode_categories": "Catégories Unicode (cliquez pour plus d'informations)",
                    "distinct_scripts": "Scripts distincts",
                    "unicode_scripts": "Scripts Unicode (cliquez pour plus d'informations)",
                    "distinct_blocks": "Blocs distincts",
                    "unicode_blocks": "Blocs Unicode (cliquez pour plus d'informations)",
                    "characters_unicode": "Caractères et Unicode",
                    "characters_unicode_caption": "Le standard Unicode attribue des propriétés de caractère à chaque point de code, qui peuvent être utilisées pour analyser les variables textuelles.",
                    "most_occurring_characters": "Caractères les plus fréquents",
                    "characters": "Caractères",
                    "categories": "Catégories",
                    "scripts": "Scripts",
                    "blocks": "Blocs",
                    "unicode": "Unicode",
                    "common_values": "Valeurs communes",
                    "common_values_table": "Valeurs communes (Tableau)",
                    "1st_row": "1ère ligne",
                    "2nd_row": "2ème ligne",
                    "3rd_row": "3ème ligne",
                    "4th_row": "4ème ligne",
                    "5th_row": "5ème ligne",
                    "categories_passes_threshold ": "Le nombre de catégories de variables dépasse le seuil (<code>config.plot.cat_freq.max_unique</code>)",
                    "common_values_plot": "Valeurs communes (Graphique)",
                    "common_words": "Mots communs",
                    "wordcloud": "Nuage de mots",
                    "words": "Mots",
                    "mean": "Moyenne",
                    "min": "Minimum",
                    "max": "Maximum",
                    "zeros": "Zéros",
                    "zeros_percentage": "Zéros (%)",
                    "scatter": "Nuage de points",
                    "scatterplot": "Nuage de points",
                    "scatterplot_caption": "Nuage de points dans le plan complexe",
                    "mini_histogram": "Mini histogramme",
                    "histogram": "Histogramme",
                    "histogram_caption": "Histogramme avec des bacs de taille fixe",
                    "extreme_values": "Valeurs extrêmes",
                    "histogram_s": "Histogramme(s)",
                    "invalid_dates": "Dates invalides",
                    "invalid_dates_percentage": "Dates invalides (%)",
                    "created": "Créé",
                    "accessed": "Accédé",
                    "modified": "Modifié",
                    "min_width": "Largeur min",
                    "median_width": "Largeur médiane",
                    "max_width": "Largeur max",
                    "min_height": "Hauteur min",
                    "median_height": "Hauteur médiane",
                    "max_height": "Hauteur max",
                    "min_area": "Aire min",
                    "median_area": "Aire médiane",
                    "max_area": "Aire max",
                    "scatter_plot_image_sizes": "Nuage de points des tailles d'images",
                    "scatter_plot": "Nuage de points",
                    "dimensions": "Dimensions",
                    "exif_keys": "Clés Exif",
                    "exif_data": "Données Exif",
                    "image": "Image",
                    "common_prefix": "Préfixe commun",
                    "unique_stems": "Radicaux uniques",
                    "unique_names": "Noms uniques",
                    "unique_extensions": "Extensions uniques",
                    "unique_directories": "Répertoires uniques",
                    "unique_anchors": "Ancres uniques",
                    "full": "Complet",
                    "stem": "Radical",
                    "name": "Nom",
                    "extension": "Extension",
                    "parent": "Parent",
                    "anchor": "Ancre",
                    "path": "Chemin",
                    "infinite": "Infini",
                    "infinite_percentage": "Infini (%)",
                    "Negative": "Négatif",
                    "Negative_percentage": "Négatif (%)",
                    "5_th_percentile": "5ème percentile",
                    "q1": "Q1",
                    "median": "médiane",
                    "q3": "Q3",
                    "95_th_percentile": "95ème percentile",
                    "range": "Étendue",
                    "iqr": "Écart interquartile (IQR)",
                    "quantile_statistics": "Statistiques de quantiles",
                    "standard_deviation": "Écart type",
                    "cv": "Coefficient de variation (CV)",
                    "kurtosis": "Kurtosis",
                    "mad": "Déviation absolue médiane (MAD)",
                    "skewness": "Asymétrie",
                    "sum": "Somme",
                    "variance": "Variance",
                    "monotonicity": "Monotonie",
                    "descriptive_statistics": "Statistiques descriptives",
                    "statistics": "Statistiques",
                    "augmented_dickey_fuller_test_value": "Valeur p du test de Dickey-Fuller augmenté",
                    "autocorrelation": "Autocorrélation",
                    "autocorrelation_caption": "ACF et PACF",
                    "timeseries": "Séries temporelles",
                    "timeseries_plot": "Graphique de séries temporelles",
                    "scheme": "Schéma",
                    "netloc": "Netloc",
                    "query": "Requête",
                    "fragment": "Fragment",
                    "heatmap": "Carte de chaleur",
                    "pearson's r": "Pearson's r",
                    "spearman's ρ": "Spearman's ρ",
                    "kendall's τ": "Kendall's τ",
                    "phik (φk)": "Phik (φk)",
                    "cramér's V (φc)": "Cramér's V (φc)",
                    "auto": "Auto"
                }
            }
        },
        "html": {
            "alerts": {
                "title": "Alertes",
                "not_present": "Alerte non présente dans ce jeu de données",
                "has_constant_value": "a une valeur constante",
                "has_constant_length": "a une longueur constante",
                "has_dirty_categories": "a des catégories sales",
                "has_high_cardinality": "a une haute cardinalité",
                "distinct_values": "valeurs distinctes",
                "dataset_has": "Le jeu de données a",
                "duplicate_rows": "lignes dupliquées",
                "dataset_is_empty": "Le jeu de données est vide",
                "is_highly": "est fortement",
                "correlated_with": "corrélé avec",
                "and": "et",
                "other_fields": "autres champs",
                "highly_imbalanced": "est fortement déséquilibré",
                "has": "a",
                "infinite_values": "valeurs infinies",
                "missing_values": "valeurs manquantes",
                "near_duplicate_rows": "lignes presque dupliquées",
                "non_stationary": "est non stationnaire",
                "seasonal": "est saisonnier",
                "highly_skewed": "est fortement asymétrique",
                "truncated_files": "fichiers tronqués",
                "alert_type_date": "contient uniquement des valeurs datetime, mais est catégorique. Considérez appliquer",
                "uniformly_distributed": "est uniformément distribué",
                "unique_values": "a des valeurs uniques",
                "alert_unsupported": "est un type non supporté, vérifiez s'il nécessite un nettoyage ou une analyse plus poussée",
                "zeros": "zéros"
            },
            "sequence": {
                "overview_tabs": {
                    "brought_to_you_by": "Créé par <a href=\"https://ydata.ai/?utm_source=opensource&utm_medium=ydataprofiling&utm_campaign=report\">YData</a>"
                }
            },
            "dropdown": "Sélectionner les colonnes",
            "frequency_table": {
                "value": "Valeur",
                "count": "Nombre",
                "frequency_percentage": "Fréquence (%)",
                "redacted_value": "Valeur masquée",
                "no_values_found": "Aucune valeur trouvée"
            },
            "scores": {
                "overall_data_quality": "Score global de qualité des données"
            },
            "variable_info": {
                "no_alerts": "Aucune alerte"
            }
        }
    }

    # 创建西班牙语翻译
    spanish_translation = {
        "report": {
            "overview": "Resumen",
            "variables": "Variables",
            "interactions": "Interacciones",
            "missing_values": "Valores faltantes",
            "sample": "Muestra",
            "duplicates": "Filas duplicadas",
            "footer_text": "Informe generado por <a href=\"https://ydata.ai/?utm_source=opensource&utm_medium=pandasprofiling&utm_campaign=report\">YData</a>.",
            "most_frequently_occurring": "Más frecuente",
            "columns": "Columnas",
            "more_details": "Más detalles"
        },
        "rendering": {
            "generate_structure": "Generar estructura del informe",
            "html_progress": "Renderizar HTML",
            "json_progress": "Renderizar JSON",
            "widgets_progress": "Renderizar widgets",
            "other_values_count": "Otros valores ({other_count})"
        },
        "core": {
            "unknown": "desconocido",
            "alerts": {
                "title": "Alertas",
                "alerts_high_correlation_tip": "Esta variable tiene una alta correlación {corr} con {num} campos: {title}",
                "correlation_types": {
                    "overall": "general"
                }
            },
            "collapse": "Colapsar",
            "container": "Contenedor",
            "correlationTable": "TablaDeCorrelacion",
            "dropdown": "Desplegable",
            "duplicate": "Duplicar",
            "html": "HTML",
            "image": "Imagen",
            "sample": "Muestra",
            "scores": "Puntuaciones",
            "table": "Tabla",
            "toggle_button": "Botón alternar",
            "variable": "Variable",
            "variable_info": "InfoVariable",
            "model": {
                "bar_count": "Recuento",
                "bar_caption": "Una visualización simple de nulidad por columna.",
                "matrix": "Matriz",
                "matrix_caption": "La matriz de nulidad es una visualización densa de datos que le permite identificar rápidamente patrones visuales en la completitud de los datos.",
                "heatmap": "Mapa de calor",
                "heatmap_caption": "El mapa de calor de correlación mide la correlación de nulidad: qué tan fuertemente la presencia o ausencia de una variable afecta la presencia de otra.",
                "first_rows": "Primeras filas",
                "last_rows": "Últimas filas",
                "random_sample": "Muestra aleatoria"
            },
            "structure": {
                "correlations": "Correlaciones",
                "heatmap": "Mapa de calor",
                "table": "Tabla",
                "overview": {
                    "values": "valores",
                    "number_variables": "Número de variables",
                    "number_observations": "Número de observaciones",
                    "number_of_series": "Número de series",
                    "missing_cells": "Celdas faltantes",
                    "missing_cells_percentage": "Celdas faltantes (%)",
                    "duplicate_rows": "Filas duplicadas",
                    "duplicate_rows_percentage": "Filas duplicadas (%)",
                    "total_size_memory": "Tamaño total en memoria",
                    "average_record_memory": "Tamaño promedio de registro en memoria",
                    "dataset_statistics": "Estadísticas del conjunto de datos",
                    "variable_types": "Tipos de variables",
                    "variable_descriptions": "Descripciones de variables",
                    "overview": "Resumen",
                    "url": "URL",
                    "copyright": "Derechos de autor",
                    "dataset": "Conjunto de datos",
                    "analysis_started": "Análisis iniciado",
                    "analysis_finished": "Análisis finalizado",
                    "duration": "Duración",
                    "software_version": "Versión del software",
                    "download_configuration": "Descargar configuración",
                    "reproduction": "Reproducción",
                    "variables": "Variables",
                    "alerts_count": "Alertas ({count})",
                    "timeseries_length": "Longitud de series temporales",
                    "starting_point": "Punto de inicio",
                    "ending_point": "Punto final",
                    "period": "Período",
                    "timeseries_statistics": "Estadísticas de series temporales",
                    "original": "Original",
                    "scaled": "Escalado",
                    "time_series": "Series temporales",
                    "interactions": "Interacciones",
                    "distinct": "Distinto",
                    "distinct_percentage": "Distinto (%)",
                    "missing": "Faltante",
                    "missing_percentage": "Faltante (%)",
                    "memory_size": "Tamaño de memoria",
                    "file": "Archivo",
                    "size": "Tamaño",
                    "file_size": "Tamaño del archivo",
                    "file_size_caption": "Histograma con bins de tamaño fijo de tamaños de archivos (en bytes)",
                    "unique": "Único",
                    "unique_help": "El número de valores únicos (todos los valores que ocurren exactamente una vez en el conjunto de datos).",
                    "unique_percentage": "Único (%)",
                    "max_length": "Longitud máx",
                    "median_length": "Longitud mediana",
                    "mean_length": "Longitud promedio",
                    "min_length": "Longitud mín",
                    "length": "Longitud",
                    "length_histogram": "histograma de longitud",
                    "histogram_lengths_category": "Histograma de longitudes de la categoría",
                    "most_occurring_categories": "Categorías más frecuentes",
                    "frequency": "Frequency",
                    "most_frequent_character_per_category": "Carácter más frecuente por categoría",
                    "most_occurring_scripts": "Scripts más frecuentes",
                    "most_frequent_character_per_script": "Carácter más frecuente por script",
                    "most_occurring_blocks": "Bloques más frecuentes",
                    "most_frequent_character_per_block": "Carácter más frecuente por bloque",
                    "imaginary": "Imaginary",
                    "real": "Real",
                    "total_characters": "Total de caracteres",
                    "distinct_characters": "Caracteres distintos",
                    "distinct_categories": "Categorías distintas",
                    "unicode_categories": "Categorías Unicode (haga clic para más información)",
                    "distinct_scripts": "Scripts distintos",
                    "unicode_scripts": "Scripts Unicode (haga clic para más información)",
                    "distinct_blocks": "Bloques distintos",
                    "unicode_blocks": "Bloques Unicode (haga clic para más información)",
                    "characters_unicode": "Caracteres y Unicode",
                    "characters_unicode_caption": "El estándar Unicode asigna propiedades de caracteres a cada punto de código, que pueden usarse para analizar variables textuales.",
                    "most_occurring_characters": "Caracteres más frecuentes",
                    "characters": "Caracteres",
                    "categories": "Categorías",
                    "scripts": "Scripts",
                    "blocks": "Bloques",
                    "unicode": "Unicode",
                    "common_values": "Valores comunes",
                    "common_values_table": "Valores comunes (Tabla)",
                    "1st_row": "1ª fila",
                    "2nd_row": "2ª fila",
                    "3rd_row": "3ª fila",
                    "4th_row": "4ª fila",
                    "5th_row": "5ª fila",
                    "categories_passes_threshold ": "El número de categorías de variables supera el umbral (<code>config.plot.cat_freq.max_unique</code>)",
                    "common_values_plot": "Valores comunes (Gráfico)",
                    "common_words": "Palabras comunes",
                    "wordcloud": "Nube de palabras",
                    "words": "Palabras",
                    "mean": "Media",
                    "min": "Mínimo",
                    "max": "Máximo",
                    "zeros": "Ceros",
                    "zeros_percentage": "Ceros (%)",
                    "scatter": "Dispersión",
                    "scatterplot": "Gráfico de dispersión",
                    "scatterplot_caption": "Gráfico de dispersión en el plano complejo",
                    "mini_histogram": "Mini histograma",
                    "histogram": "Histograma",
                    "histogram_caption": "Histograma con bins de tamaño fijo",
                    "extreme_values": "Valores extremos",
                    "histogram_s": "Histograma(s)",
                    "invalid_dates": "Fechas inválidas",
                    "invalid_dates_percentage": "Fechas inválidas (%)",
                    "created": "Creado",
                    "accessed": "Accedido",
                    "modified": "Modificado",
                    "min_width": "Ancho mín",
                    "median_width": "Ancho mediano",
                    "max_width": "Ancho máx",
                    "min_height": "Alto mín",
                    "median_height": "Alto mediano",
                    "max_height": "Alto máx",
                    "min_area": "Área mín",
                    "median_area": "Área mediana",
                    "max_area": "Área máx",
                    "scatter_plot_image_sizes": "Gráfico de dispersión de tamaños de imágenes",
                    "scatter_plot": "Gráfico de dispersión",
                    "dimensions": "Dimensiones",
                    "exif_keys": "Claves Exif",
                    "exif_data": "Datos Exif",
                    "image": "Imagen",
                    "common_prefix": "Prefijo común",
                    "unique_stems": "Raíces únicas",
                    "unique_names": "Nombres únicos",
                    "unique_extensions": "Extensiones únicas",
                    "unique_directories": "Directorios únicos",
                    "unique_anchors": "Anclas únicas",
                    "full": "Completo",
                    "stem": "Raíz",
                    "name": "Nombre",
                    "extension": "Extensión",
                    "parent": "Padre",
                    "anchor": "Ancla",
                    "path": "Ruta",
                    "infinite": "Infinito",
                    "infinite_percentage": "Infinito (%)",
                    "Negative": "Negativo",
                    "Negative_percentage": "Negativo (%)",
                    "5_th_percentile": "Percentil 5",
                    "q1": "Q1",
                    "median": "mediana",
                    "q3": "Q3",
                    "95_th_percentile": "Percentil 95",
                    "range": "Rango",
                    "iqr": "Rango intercuartílico (IQR)",
                    "quantile_statistics": "Estadísticas de cuantiles",
                    "standard_deviation": "Desviación estándar",
                    "cv": "Coeficiente de variación (CV)",
                    "kurtosis": "Curtosis",
                    "mad": "Desviación absoluta mediana (MAD)",
                    "skewness": "Asimetría",
                    "sum": "Suma",
                    "variance": "Varianza",
                    "monotonicity": "Monotonicidad",
                    "descriptive_statistics": "Estadísticas descriptivas",
                    "statistics": "Estadísticas",
                    "augmented_dickey_fuller_test_value": "Valor p de la prueba Dickey-Fuller aumentada",
                    "autocorrelation": "Autocorrelación",
                    "autocorrelation_caption": "ACF y PACF",
                    "timeseries": "Series temporales",
                    "timeseries_plot": "Gráfico de series temporales",
                    "scheme": "Esquema",
                    "netloc": "Netloc",
                    "query": "Consulta",
                    "fragment": "Fragmento",
                    "heatmap": "Mapa de calor",
                    "pearson's r": "Pearson's r",
                    "spearman's ρ": "Spearman's ρ",
                    "kendall's τ": "Kendall's τ",
                    "phik (φk)": "Phik (φk)",
                    "cramér's V (φc)": "Cramér's V (φc)",
                    "auto": "Auto"
                }
            }
        },
        "html": {
            "alerts": {
                "title": "Alertas",
                "not_present": "Alerta no presente en este conjunto de datos",
                "has_constant_value": "tiene valor constante",
                "has_constant_length": "tiene longitud constante",
                "has_dirty_categories": "tiene categorías sucias",
                "has_high_cardinality": "tiene alta cardinalidad",
                "distinct_values": "valores distintos",
                "dataset_has": "El conjunto de datos tiene",
                "duplicate_rows": "filas duplicadas",
                "dataset_is_empty": "El conjunto de datos está vacío",
                "is_highly": "está altamente",
                "correlated_with": "correlacionado con",
                "and": "y",
                "other_fields": "otros campos",
                "highly_imbalanced": "está altamente desbalanceado",
                "has": "tiene",
                "infinite_values": "valores infinitos",
                "missing_values": "valores faltantes",
                "near_duplicate_rows": "filas casi duplicadas",
                "non_stationary": "es no estacionario",
                "seasonal": "es estacional",
                "highly_skewed": "está altamente sesgado",
                "truncated_files": "archivos truncados",
                "alert_type_date": "solo contiene valores datetime, pero es categórico. Considere aplicar",
                "uniformly_distributed": "está uniformemente distribuido",
                "unique_values": "tiene valores únicos",
                "alert_unsupported": "es un tipo no soportado, verifique si necesita limpieza o análisis adicional",
                "zeros": "ceros"
            },
            "sequence": {
                "overview_tabs": {
                    "brought_to_you_by": "Desarrollado por <a href=\"https://ydata.ai/?utm_source=opensource&utm_medium=ydataprofiling&utm_campaign=report\">YData</a>"
                }
            },
            "dropdown": "Seleccionar columnas",
            "frequency_table": {
                "value": "Valor",
                "count": "Recuento",
                "frequency_percentage": "Frecuencia (%)",
                "redacted_value": "Valor censurado",
                "no_values_found": "No se encontraron valores"
            },
            "scores": {
                "overall_data_quality": "Puntuación general de calidad de datos"
            },
            "variable_info": {
                "no_alerts": "Sin alertas"
            }
        }
    }

    # 保存翻译文件
    french_file = OUTPUT_DIR / "french_translation.json"
    spanish_file = OUTPUT_DIR / "spanish_translation.json"

    with open(french_file, 'w', encoding='utf-8') as f:
        json.dump(french_translation, f, indent=2, ensure_ascii=False)

    with open(spanish_file, 'w', encoding='utf-8') as f:
        json.dump(spanish_translation, f, indent=2, ensure_ascii=False)

    print(f"✅ French translation saved to: {french_file}")
    print(f"✅ Spanish translation saved to: {spanish_file}")

    return french_file, spanish_file


def step3_test_translation_function():
    """步骤3: 测试翻译函数"""
    print(f"\n🧪 Step 3: Testing translation function...")

    # 测试基本翻译功能
    print("📋 Current available locales:", get_available_locales())
    print("🌍 Current locale:", get_locale())

    # 测试一些翻译键
    test_keys = [
        "report.overview",
        "report.variables",
        "core.alerts.title",
        "html.frequency_table.value",
        "nonexistent.key"
    ]

    print("\n🔍 Testing translation keys:")
    for key in test_keys:
        translation = _(key)
        print(f"  {key} → {translation}")


def step4_single_file_loading(df, french_file):
    """步骤4: 单个翻译文件加载示例"""
    print(f"\n📁 Step 4: Loading single translation file - {french_file}")

    # 加载法语翻译
    load_translation_file(french_file, 'fr')

    print(f"📋 Available locales after loading: {get_available_locales()}")

    # 设置为法语并生成报告
    set_locale('fr')
    print(f"🌍 Current locale set to: {get_locale()}")

    # 测试翻译
    print(f"🔍 Testing French translations:")
    print(f"  report.overview → {_('report.overview')}")
    print(f"  core.alerts.title → {_('core.alerts.title')}")

    profile = ProfileReport(
        df,
        title="Rapport d'Analyse des Produits Smartphones",
        interactions={
            "continuous": True,
            "targets": []
        },
        vars={
            "num": {
                "low_categorical_threshold": 0,  # 设为0，避免数值列被误判为分类
            }
        },
        minimal=False  # 生成详细版本
    )
    output_file = OUTPUT_DIR / "product_analysis_french.html"

    # 强制覆盖生成报告
    try:
        profile.to_file(output_file)
        print(f"✅ French report generated: {output_file}")
    except Exception as e:
        print(f"⚠️ Warning generating French report: {e}")
        # 如果报告生成失败，删除已存在的文件再重试
        if Path(output_file).exists():
            Path(output_file).unlink()
        profile.to_file(output_file)
        print(f"✅ French report generated (after cleanup): {output_file}")

    return output_file


def step5_directory_loading(df, french_file, spanish_file):
    """步骤5: 翻译目录加载示例"""
    print(f"\n📂 Step 5: Loading translation directory")

    # 创建翻译目录在output中
    translations_dir = OUTPUT_DIR / "custom_translations"
    translations_dir.mkdir(exist_ok=True)

    # 目标文件路径
    french_target = translations_dir / "fr.json"
    spanish_target = translations_dir / "es.json"

    # 复制文件而不是移动，避免文件已存在的错误
    try:
        shutil.copy2(french_file, french_target)
        print(f"📄 Copied {french_file} to {french_target}")
    except Exception as e:
        print(f"⚠️ Warning copying French file: {e}")
        # 如果复制失败，直接覆盖
        shutil.copyfile(french_file, french_target)

    try:
        shutil.copy2(spanish_file, spanish_target)
        print(f"📄 Copied {spanish_file} to {spanish_target}")
    except Exception as e:
        print(f"⚠️ Warning copying Spanish file: {e}")
        # 如果复制失败，直接覆盖
        shutil.copyfile(spanish_file, spanish_target)

    print(f"📁 Created translation directory: {translations_dir}")
    print(f"📄 Files in directory: {list(translations_dir.glob('*.json'))}")

    # 加载整个翻译目录
    add_translation_directory(translations_dir)

    print(f"📋 Available locales after directory loading: {get_available_locales()}")

    # 生成西班牙语报告
    set_locale('es')
    print(f"🌍 Current locale set to: {get_locale()}")

    # 测试西班牙语翻译
    print(f"🔍 Testing Spanish translations:")
    print(f"  report.overview → {_('report.overview')}")
    print(f"  core.alerts.title → {_('core.alerts.title')}")

    profile = ProfileReport(
        df,
        title="Informe de Análisis de Productos Smartphones",
        plot={"font": {"chinese_support": True}},
        interactions={
            "continuous": True,
            "targets": []
        },
        vars={
            "num": {
                "low_categorical_threshold": 0,  # 设为0，避免数值列被误判为分类
            }
        },
        minimal=False  # 生成详细版本
    )
    output_file = OUTPUT_DIR / "product_analysis_spanish.html"

    # 强制覆盖生成报告
    try:
        profile.to_file(output_file)
        print(f"✅ Spanish report generated: {output_file}")
    except Exception as e:
        print(f"⚠️ Warning generating Spanish report: {e}")
        # 如果报告生成失败，删除已存在的文件再重试
        if Path(output_file).exists():
            Path(output_file).unlink()
        profile.to_file(output_file)
        print(f"✅ Spanish report generated (after cleanup): {output_file}")

    return output_file, translations_dir


def step6_builtin_chinese_support(df):
    """步骤6: 内置中文支持测试"""
    print(f"\n🇨🇳 Step 6: Testing built-in Chinese support")

    # 直接使用内置的中文支持
    set_locale('zh')
    print(f"🌍 Current locale set to: {get_locale()}")

    # 测试中文翻译（如果存在）
    print(f"🔍 Testing Chinese translations:")
    print(f"  report.overview → {_('report.overview')}")
    print(f"  report.variables → {_('report.variables')}")

    profile = ProfileReport(
        df,
        title="用电分析报告",
        # plot={"font": {"chinese_support": True}},
        plot={"font": {"custom_font_path": "C:\Windows\Fonts\simhei.ttf"}},
        locale='zh',
        interactions={
            "continuous": True,
            "targets": []
        },
        vars={
            "num": {
                "low_categorical_threshold": 0,  # 设为0，避免数值列被误判为分类
            }
        },
        minimal=False  # 生成详细版本
    )
    output_file = OUTPUT_DIR / "product_analysis_chinese.html"

    # 强制覆盖生成报告
    try:
        profile.to_file(output_file)
        print(f"✅ Chinese report generated: {output_file}")
    except Exception as e:
        print(f"⚠️ Warning generating Chinese report: {e}")
        # 如果报告生成失败，删除已存在的文件再重试
        if Path(output_file).exists():
            Path(output_file).unlink()
        profile.to_file(output_file)
        print(f"✅ Chinese report generated (after cleanup): {output_file}")

    return output_file


def step7_locale_parameter_usage(df):
    """步骤7: 使用ProfileReport的locale参数"""
    print(f"\n⚙️ Step 7: Using ProfileReport locale parameter")

    # 重置为英文
    set_locale('en')
    print(f"🔄 Reset global locale to: {get_locale()}")

    # 直接在ProfileReport中指定语言（如果支持）
    print("🔄 Generating report with explicit locale parameters...")

    # 生成英文报告
    profile_en = ProfileReport(
        df,
        title="Smartphone Products Analysis Report",
        plot={"font": {"chinese_support": True}},
        interactions={
            "continuous": True,
            "targets": []
        },
        vars={
            "num": {
                "low_categorical_threshold": 0,  # 设为0，避免数值列被误判为分类
            }
        },
        minimal=False
    )
    output_file_en = OUTPUT_DIR / "product_analysis_explicit_english.html"
    profile_en.to_file(output_file_en)

    print(f"✅ English report generated: {output_file_en}")
    print(f"🌍 Global locale remains: {get_locale()}")

    return output_file_en


def cleanup_files(files_to_clean):
    """清理生成的文件"""
    print(f"\n🧹 Cleaning up generated files...")

    for file_path in files_to_clean:
        try:
            if isinstance(file_path, str):
                file_path = Path(file_path)

            if file_path.exists():
                if file_path.is_file():
                    file_path.unlink()
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
                print(f"🗑️ Removed: {file_path}")
        except Exception as e:
            print(f"⚠️ Could not remove {file_path}: {e}")

    # 尝试删除output目录（如果为空）
    try:
        if OUTPUT_DIR.exists() and not any(OUTPUT_DIR.iterdir()):
            OUTPUT_DIR.rmdir()
            print(f"🗑️ Removed empty output directory: {OUTPUT_DIR}")
    except Exception as e:
        print(f"⚠️ Could not remove output directory: {e}")


def diagnose_font_issues():
    """诊断字体配置问题"""
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    import platform

    print("=" * 50)
    print("字体配置诊断报告")
    print("=" * 50)

    # 1. 系统信息
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"Python版本: {platform.python_version()}")

    # 2. 当前matplotlib字体配置
    print(f"\n当前字体配置:")
    print(f"font.sans-serif: {plt.rcParams['font.sans-serif'][:5]}...")  # 只显示前5个
    print(f"font.family: {plt.rcParams['font.family']}")
    print(f"axes.unicode_minus: {plt.rcParams['axes.unicode_minus']}")

    # 3. 检查系统中可用的中文字体
    print(f"\n系统中的字体总数: {len(fm.fontManager.ttflist)}")

    chinese_fonts = []
    for font in fm.fontManager.ttflist:
        font_name = font.name
        if any(keyword in font_name.lower() for keyword in
               ['simhei', 'yahei', 'simsun', 'pingfang', 'heiti', 'wenquanyi', 'noto']):
            chinese_fonts.append(font_name)

    print(f"发现的中文字体:")
    for font in chinese_fonts[:10]:  # 只显示前10个
        print(f"  - {font}")

    if not chinese_fonts:
        print("  ❌ 未找到中文字体!")

    # 4. 测试具体字体
    test_fonts = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans', 'Arial']
    print(f"\n字体可用性测试:")

    for font_name in test_fonts:
        try:
            font = fm.FontProperties(family=font_name)
            actual_font = fm.findfont(font)
            print(f"  {font_name}: ✅ -> {actual_font}")
        except Exception as e:
            print(f"  {font_name}: ❌ -> {e}")

    return chinese_fonts


def main():
    """主函数 - 演示完整的翻译工作流程"""
    print("🚀 YData Profiling Multilingual Advanced Example")
    print("=" * 60)
    print("📝 This example demonstrates:")
    print("   • Translation template export")
    print("   • Custom translation creation")
    print("   • Single file and directory loading")
    print("   • Built-in language support")
    print("   • Report generation in multiple languages")
    print("=" * 60)
    setup_chinese_fonts()
    diagnose_font_issues()
    # 设置输出目录
    output_dir = setup_output_directory()

    # 记录要清理的文件
    files_to_clean = []

    try:
        print("🔧 配置中文字体支持...")
        font_success = setup_chinese_fonts()

        # 创建示例数据
        df = create_sample_data()

        # 步骤1: 导出模板
        template_file = step1_export_template()
        files_to_clean.append(template_file)

        # 步骤2: 创建自定义翻译
        french_file, spanish_file = step2_create_custom_translations(template_file)
        files_to_clean.extend([french_file, spanish_file])

        # 步骤3: 测试翻译功能
        step3_test_translation_function()

        # 步骤4: 单文件加载
        french_report = step4_single_file_loading(df, french_file)
        files_to_clean.append(french_report)

        # 步骤5: 目录加载
        spanish_report, translations_dir = step5_directory_loading(df, french_file, spanish_file)
        files_to_clean.extend([spanish_report, translations_dir])

        # 步骤6: 内置中文支持
        chinese_report = step6_builtin_chinese_support(df)
        files_to_clean.append(chinese_report)

        # 步骤7: 显式locale参数
        english_report = step7_locale_parameter_usage(df)
        files_to_clean.append(english_report)

        print(f"\n🎉 All steps completed successfully!")
        print(f"📊 Generated files in {output_dir}:")
        for file in files_to_clean:
            relative_path = file.relative_to(Path.cwd()) if isinstance(file, Path) else file
            if isinstance(file, Path) and file.is_file():
                print(f"   ✅ {relative_path}")
            elif isinstance(file, Path) and file.is_dir():
                print(f"   📁 {relative_path}/ (directory)")
            else:
                print(f"   📄 {relative_path}")

        print(f"\n📍 All files are located in: {output_dir.absolute()}")
        print(f"💡 You can open the HTML files in your browser to see the multilingual reports.")
        print(f"🔍 Compare the reports to see the translation differences.")

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # 询问是否清理文件
        try:
            response = input(f"\n🤔 Do you want to clean up generated files? (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                cleanup_files(files_to_clean)
                print("✨ Cleanup completed!")
            else:
                print("📁 Files kept for your review.")
                print(f"📍 Location: {output_dir.absolute()}")
                print("💡 Tip: You can run this script multiple times to test the overwrites.")
        except KeyboardInterrupt:
            print(f"\n📁 Files kept for your review.")
            print(f"📍 Location: {output_dir.absolute()}")


if __name__ == "__main__":
    main()
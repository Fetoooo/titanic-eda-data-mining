import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets cell background shading."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets padding for a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3"):
    """Applies clean horizontal borders to table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>\n'
        f'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="1B365D"/>\n'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_report():
    doc = Document()

    # Configure Margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header & Footer
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_ft.text = "Assignment 1 – Data Mining (26/27) | Page "

    # Color Palette Definitions
    COLOR_PRIMARY = RGBColor(27, 54, 93)     # Deep Navy #1B365D
    COLOR_SECONDARY = RGBColor(70, 130, 180) # Steel Blue #4682B4
    COLOR_DARK = RGBColor(34, 34, 34)        # Charcoal #222222
    COLOR_MUTED = RGBColor(100, 100, 100)    # Gray #646464
    HEX_PRIMARY = "1B365D"
    HEX_LIGHT_BG = "F4F7FA"
    HEX_BORDER = "CCCCCC"

    # Set Normal Style Font
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Calibri'
    font_normal.size = Pt(11)
    font_normal.color.rgb = COLOR_DARK

    # Document Header Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    title_run = title_p.add_run("ASSIGNMENT 1 – DATA MINING (26/27)")
    title_run.font.size = Pt(11)
    title_run.font.bold = True
    title_run.font.color.rgb = COLOR_SECONDARY

    main_title = doc.add_paragraph()
    main_title.paragraph_format.space_before = Pt(0)
    main_title.paragraph_format.space_after = Pt(6)
    t_run = main_title.add_run("Data Preprocessing, Analysis, and Visualization")
    t_run.font.size = Pt(22)
    t_run.font.bold = True
    t_run.font.color.rgb = COLOR_PRIMARY

    sub_title = doc.add_paragraph()
    sub_title.paragraph_format.space_before = Pt(0)
    sub_title.paragraph_format.space_after = Pt(14)
    s_run = sub_title.add_run("A Comprehensive End-to-End Study on the Titanic Passenger Dataset Using Python")
    s_run.font.size = Pt(13)
    s_run.font.italic = True
    s_run.font.color.rgb = COLOR_MUTED

    # Student & Submission Metadata Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table, "B0C4DE")

    metadata = [
        ("Student Name:", "Fathy Ayman Fathy"),
        ("Section Number:", "Section 3"),
        ("Course & Academic Term:", "Data Mining – Academic Year 26/27"),
        ("Dataset & Source:", "Titanic Survival Dataset (Seaborn Official Repository / Vanderbilt Biostatistics / Kaggle)")
    ]

    for i, (label, val) in enumerate(metadata):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        
        set_cell_background(c0, "F0F4F8")
        set_cell_background(c1, "FAFCFD")

        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(10)
        r0.font.color.rgb = COLOR_PRIMARY

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.size = Pt(10)
        if i in [0, 1]:  # Student Name and Section
            r1.font.bold = True
            r1.font.color.rgb = COLOR_PRIMARY
        else:
            r1.font.color.rgb = COLOR_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------
    # SECTION 1: Dataset Description & Selection
    # -------------------------------------------------------------
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(4)
    h1_run = h1.add_run("1. Dataset Selection and Description")
    h1_run.font.size = Pt(15)
    h1_run.font.bold = True
    h1_run.font.color.rgb = COLOR_PRIMARY

    p_desc = doc.add_paragraph()
    p_desc.add_run(
        "For this assignment, we selected the renowned Titanic Passenger Survival Dataset. "
        "The exact dataset source is the official Seaborn data repository (https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv), "
        "derived from historical manifests compiled by Thomas Cason and archived at the Vanderbilt University Department of Biostatistics and Kaggle.\n\n"
        "The primary analytical purpose of this dataset is to investigate passenger demographics, socioeconomic stratification, "
        "and travel characteristics to uncover the key factors that influenced passenger survival rates during the disaster."
    )

    # Requirement Verification Table
    h2_req = doc.add_paragraph()
    h2_req.paragraph_format.space_before = Pt(8)
    h2_req.paragraph_format.space_after = Pt(4)
    h2_run = h2_req.add_run("1.1 Compliance with Assignment Requirements")
    h2_run.font.size = Pt(12)
    h2_run.font.bold = True
    h2_run.font.color.rgb = COLOR_SECONDARY

    req_table = doc.add_table(rows=5, cols=3)
    req_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(req_table, HEX_BORDER)

    headers = ["Assignment Requirement", "Titanic Dataset Attribute", "Compliance Status"]
    for j, h in enumerate(headers):
        cell = req_table.rows[0].cells[j]
        set_cell_background(cell, HEX_PRIMARY)
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    req_data = [
        ("At least 300 rows and 6 columns", "891 rows and 15 columns", "Fully Satisfied (Exceeds requirement)"),
        ("At least 3 numerical columns", "6 numerical: survived, pclass, age, sibsp, parch, fare", "Fully Satisfied"),
        ("At least 2 categorical columns", "7 categorical: sex, embarked, class, who, deck, embark_town, alive", "Fully Satisfied"),
        ("Contains missing values for cleaning", "deck (688 nulls), age (177 nulls), embarked (2 nulls)", "Fully Satisfied (Authentic nulls)")
    ]

    for i, row in enumerate(req_data):
        r_cells = req_table.rows[i+1].cells
        for j, text in enumerate(row):
            r_cells[j].paragraphs[0].paragraph_format.space_after = Pt(0)
            set_cell_margins(r_cells[j], 60, 60, 80, 80)
            if i % 2 == 1:
                set_cell_background(r_cells[j], HEX_LIGHT_BG)
            r = r_cells[j].paragraphs[0].add_run(text)
            r.font.size = Pt(9)
            if j == 2:
                r.font.bold = True
                r.font.color.rgb = RGBColor(40, 140, 40)

    # -------------------------------------------------------------
    # SECTION 2: Data Exploration Summary
    # -------------------------------------------------------------
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(16)
    h2.paragraph_format.space_after = Pt(4)
    h2_run = h2.add_run("2. Data Exploration Summary")
    h2_run.font.size = Pt(15)
    h2_run.font.bold = True
    h2_run.font.color.rgb = COLOR_PRIMARY

    p_exp = doc.add_paragraph()
    p_exp.add_run(
        "In strict compliance with Part 2 instructions, exploratory data analysis was conducted exclusively using native Pandas operations:\n"
        "1. Displaying First & Last Rows: Executed using df.head(7) and df.tail(7) to inspect initial structure and sample records.\n"
        "2. Displaying Rows & Columns: Extracted using the Pandas DataFrame attribute df.shape (891 rows, 15 columns).\n"
        "3. Column Data Types & Structure: Audited using df.dtypes and df.info() (6 numerical, 7 categorical, 2 boolean).\n"
        "4. Descriptive Statistics: Computed using df.describe() for numerical attributes and df.describe(include=['object', 'category', 'bool']) for categorical attributes.\n"
        "5. Checking Missing Values: Quantified per column using Pandas boolean masking df.isnull().sum() and percentage calculations.\n"
        "6. Checking Duplicated Rows: Identified using the Pandas method df.duplicated().sum() (107 duplicate rows across all 15 raw features).\n"
        "7. Exploratory Visualizations: Produced using Pandas' native plotting engine df.plot(kind='bar') to examine missing value frequencies and target survival balance."
    )

    # Descriptive Statistics Summary Table
    h2_stats = doc.add_paragraph()
    h2_stats.paragraph_format.space_before = Pt(6)
    h2_stats.paragraph_format.space_after = Pt(4)
    h2_stats_run = h2_stats.add_run("2.1 Key Descriptive Statistics (Numerical Features in Code)")
    h2_stats_run.font.size = Pt(11)
    h2_stats_run.font.bold = True
    h2_stats_run.font.color.rgb = COLOR_SECONDARY

    stat_table = doc.add_table(rows=7, cols=6)
    stat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(stat_table, HEX_BORDER)

    stat_headers = ["Raw Column Name", "Mean", "Std. Dev.", "Min", "Median (50%)", "Max"]
    for j, h in enumerate(stat_headers):
        c = stat_table.rows[0].cells[j]
        set_cell_background(c, HEX_PRIMARY)
        set_cell_margins(c, 70, 70, 80, 80)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9)

    stats_rows = [
        ("survived", "0.384", "0.487", "0.000", "0.000", "1.000"),
        ("pclass", "2.309", "0.836", "1.000", "3.000", "3.000"),
        ("age", "29.699", "14.526", "0.420", "28.000", "80.000"),
        ("sibsp", "0.523", "1.103", "0.000", "0.000", "8.000"),
        ("parch", "0.382", "0.806", "0.000", "0.000", "6.000"),
        ("fare", "32.204", "49.693", "0.000", "14.454", "512.329")
    ]

    for i, row in enumerate(stats_rows):
        r_cells = stat_table.rows[i+1].cells
        for j, text in enumerate(row):
            r_cells[j].paragraphs[0].paragraph_format.space_after = Pt(0)
            set_cell_margins(r_cells[j], 50, 50, 70, 70)
            if i % 2 == 1:
                set_cell_background(r_cells[j], HEX_LIGHT_BG)
            r = r_cells[j].paragraphs[0].add_run(text)
            r.font.size = Pt(8.5)
            if j == 0:
                r.font.bold = True

    # -------------------------------------------------------------
    # SECTION 3: Data Cleaning and Preprocessing
    # -------------------------------------------------------------
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(16)
    h3.paragraph_format.space_after = Pt(4)
    h3_run = h3.add_run("3. Summary of Preprocessing Operations Performed")
    h3_run.font.size = Pt(15)
    h3_run.font.bold = True
    h3_run.font.color.rgb = COLOR_PRIMARY

    p_pre = doc.add_paragraph()
    p_pre.add_run(
        "To prepare the raw dataset for rigorous data mining, five systematic preprocessing operations "
        "were implemented. Below is a comprehensive explanation of each operation's rationale and its observed effect on the data:"
    )

    # Preprocessing Operations Table
    pre_table = doc.add_table(rows=6, cols=4)
    pre_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(pre_table, HEX_BORDER)

    p_headers = ["#", "Preprocessing Operation", "Rationale (Why Performed)", "Effect on Dataset"]
    widths = [Inches(0.4), Inches(1.8), Inches(2.5), Inches(1.8)]

    for j, h in enumerate(p_headers):
        c = pre_table.rows[0].cells[j]
        c.width = widths[j]
        set_cell_background(c, HEX_PRIMARY)
        set_cell_margins(c, 80, 80, 90, 90)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9)

    prep_data = [
        (
            "1",
            "Handling Missing Values (Imputation)",
            "Continuous 'Age' exhibited skewness; imputing via conditional group medians (by Pclass and Sex) preserves demographic reality (1st class passengers were older). Categorical 'Embarked' (2 nulls) was imputed using statistical mode ('S').",
            "Missing values in 'Age' dropped from 177 to 0; missing in 'Embarked' dropped from 2 to 0. Zero missing values remain in retained columns."
        ),
        (
            "2",
            "Dropping Redundant & Sparse Columns",
            "'deck' was missing >77.2% of entries (imputation introduces extreme artificial bias). 'alive', 'class', 'embark_town', 'who', and 'adult_male' are exact duplicate or derived representations of other columns.",
            "Column count reduced from 15 to 9. Removed multicollinearity and severe sparsity without losing analytical information."
        ),
        (
            "3",
            "Identifying & Removing Duplicate Rows",
            "Duplicate Counting Clarification: Evaluating across all 15 raw attributes initially identified 107 duplicate rows. Following Operation 2's removal of 6 redundant columns, identical records across the remaining 9 features increased to 118 (the original 107 full duplicates + 11 records differing only in discarded redundant columns). Removing these prevents artificial repetition.",
            "118 duplicate rows removed (107 full-row + 11 post-column pruning). Cleaned dataset reduced from 891 to 773 unique passenger records (0 duplicates remaining)."
        ),
        (
            "4",
            "Column Renaming & Type Casting",
            "Column names standardized to Title_Case for professional readability. 'Age' cast to integer (int64) to eliminate fractional years; 'Is_Alone' converted from boolean to integer (1/0).",
            "Enhanced readability and computational compatibility across numerical data pipelines."
        ),
        (
            "5",
            "Categorical to Numerical Encoding",
            "Data mining algorithms (correlation, regression, clustering) require numerical inputs. 'Gender' mapped to binary (male=0, female=1) and 'Embarkation_Port' label-encoded (S=0, C=1, Q=2).",
            "Features became directly usable in Pearson correlation matrix and mathematical modeling."
        )
    ]

    for i, row in enumerate(prep_data):
        r_cells = pre_table.rows[i+1].cells
        for j, text in enumerate(row):
            r_cells[j].width = widths[j]
            r_cells[j].paragraphs[0].paragraph_format.space_after = Pt(0)
            set_cell_margins(r_cells[j], 60, 60, 80, 80)
            if i % 2 == 1:
                set_cell_background(r_cells[j], HEX_LIGHT_BG)
            r = r_cells[j].paragraphs[0].add_run(text)
            r.font.size = Pt(8.5)
            if j == 0 or j == 1:
                r.font.bold = True

    # -------------------------------------------------------------
    # SECTION 4: Data Selection and Manipulation Highlights
    # -------------------------------------------------------------
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(16)
    h4.paragraph_format.space_after = Pt(4)
    h4_run = h4.add_run("4. Data Selection and Manipulation Highlights")
    h4_run.font.size = Pt(15)
    h4_run.font.bold = True
    h4_run.font.color.rgb = COLOR_PRIMARY

    p_sel = doc.add_paragraph()
    p_sel.add_run(
        "Part 4 of the assignment demonstrated core Pandas indexing and transformation capabilities:\n\n"
        "1. Label-Based vs. Position-Based Indexing:\n"
        "   • loc[] selects data by index and column labels (e.g. df.loc[10:15, ['Gender', 'Age', 'Fare']]). "
        "Importantly, label-based slicing is endpoint-inclusive.\n"
        "   • iloc[] selects data strictly by zero-indexed integer offsets (e.g. df.iloc[0:5, [0, 1, 3, 6]]). "
        "Position-based slicing is half-open (excludes endpoint).\n\n"
        "2. The Critical Numerical Index Distinction:\n"
        "   When a DataFrame is filtered (e.g., elderly_df = df[df['Age'] > 70]), index labels retain their original values "
        "(e.g., [78, 97, 395, 423, 747]). In this scenario, elderly_df.loc[97] searches for the label '97', whereas "
        "elderly_df.iloc[1] retrieves the second row in the table (which happens to carry label 97). Attempting to call "
        "elderly_df.iloc[97] triggers an IndexError because the filtered table contains only 5 rows. This demonstrates why "
        "understanding label vs. position indexing is paramount in data mining.\n\n"
        "3. Analytical Groupby Findings:\n"
        "   Using df.groupby(['Passenger_Class', 'Gender'])[['Survived', 'Fare', 'Age']].agg({'Survived': ['mean', 'count'], 'Fare': 'mean', 'Age': 'mean'}), "
        "we answered key socio-historical questions: First-class women paid an average fare of £104.99 and achieved a 96.7% survival rate, "
        "whereas third-class men paid an average fare of £12.16 and experienced only a 13.5% survival rate."
    )

    # -------------------------------------------------------------
    # SECTION 5: Visualizations & In-Depth Explanations
    # -------------------------------------------------------------
    doc.add_page_break()

    h5 = doc.add_paragraph()
    h5.paragraph_format.space_before = Pt(10)
    h5.paragraph_format.space_after = Pt(4)
    h5_run = h5.add_run("5. Data Visualizations and Detailed Observations")
    h5_run.font.size = Pt(16)
    h5_run.font.bold = True
    h5_run.font.color.rgb = COLOR_PRIMARY

    p_vis_intro = doc.add_paragraph()
    p_vis_intro.add_run(
        "In accordance with the assignment specifications and lecture slides on visual data mining, "
        "we present five distinctly different chart types (Bar Chart, Histogram with KDE, Box Plot, Scatter Plot, and Heatmap). "
        "Below each visualization, 2–3 sentences explain what the visualization shows followed by a concrete analytical observation."
    )

    # Visualizations Data Dictionary
    visuals_info = [
        {
            "num": "1",
            "title": "Figure 1: Passenger Survival Rate by Travel Class and Gender",
            "type": "Bar Chart (Categorical vs. Numerical Comparison)",
            "image": "figures/figure1_bar_chart.png",
            "shows": "This bar chart displays the mean survival rate (proportion of survivors) segmented across the three passenger travel classes (First, Second, Third), subdivided by passenger gender (Female vs. Male). The vertical axis represents survival percentage from 0% to 100%, with exact percentages annotated above each bar.",
            "observation": "Female passengers in First Class exhibited an overwhelming survival rate of 96.7%, and Second Class females survived at 91.9%, whereas Third Class males survived at merely 13.5%. This provides compelling empirical evidence that while the historical maritime protocol ('women and children first') was enforced, socioeconomic travel tier played a critical role in evacuation survival."
        },
        {
            "num": "2",
            "title": "Figure 2: Passenger Age Distribution by Survival Outcome (with KDE)",
            "type": "Histogram with Kernel Density Estimation (Continuous Distribution)",
            "image": "figures/figure2_histogram.png",
            "shows": "This histogram illustrates the frequency distribution and continuous kernel density estimate (KDE) of passenger ages, layered by survival outcome (Green = Survived, Red = Did Not Survive). The horizontal axis spans passenger ages from 0 to 80 years across 30 equal bins, while the vertical axis shows passenger headcounts.",
            "observation": "The distribution reveals that the largest passenger concentration consisted of young adults aged 20 to 35, who experienced the highest absolute casualty rates. Conversely, a prominent survival peak is visible among children aged 0 to 8 years, confirming that lifeboats actively prioritized infants and young children."
        },
        {
            "num": "3",
            "title": "Figure 3: Ticket Fare Distribution Across Passenger Classes",
            "type": "Box Plot (Five-Number Summary & Outlier Detection)",
            "image": "figures/figure3_box_plot.png",
            "shows": "This box plot summarizes the distribution of ticket fares across the three travel classes using the five-number summary: minimum, first quartile (Q1), median, third quartile (Q3), and maximum. The vertical fare axis is displayed on a logarithmic scale to properly capture the wide spread of ticket prices.",
            "observation": "First Class fares demonstrate vastly greater median values and interquartile dispersion than Second and Third Class, alongside substantial upper outliers reaching over £500. In contrast, Third Class ticket fares are tightly compressed between £7 and £15, illustrating the severe economic divide aboard the vessel."
        },
        {
            "num": "4",
            "title": "Figure 4: Passenger Age vs. Ticket Fare by Survival Status",
            "type": "Scatter Plot (Bivariate Numerical Relationship)",
            "image": "figures/figure4_scatter_plot.png",
            "shows": "This scatter plot plots individual passengers according to their continuous age on the horizontal x-axis and their ticket fare paid on the vertical y-axis. Data points are distinguished by survival outcome using dual encoding: green circles denote survivors, while red 'X' markers denote non-survivors.",
            "observation": "Passengers paying premium fares exceeding £100 are almost exclusively green circles, demonstrating near-perfect survival among elite ticket holders across all adult age brackets. In stark contrast, the dense cluster of passengers with fares under £30 shows extensive mortality across children, young adults, and elderly travelers alike."
        },
        {
            "num": "5",
            "title": "Figure 5: Correlation Matrix Heatmap of Preprocessed Titanic Features",
            "type": "Heatmap (Correlation Matrix Visualization)",
            "image": "figures/figure5_correlation_heatmap.png",
            "shows": "This heatmap illustrates the pairwise Pearson linear correlation coefficients between all cleaned numerical and encoded features, including Survived, Passenger_Class, Gender_Code, Age, Siblings_Spouses, Parents_Children, Fare, and Port_Code. A diverging colormap is employed with numerical annotations directly displayed in each cell.",
            "observation": "The strongest single positive linear predictor of survival is Gender_Code (r = +0.50), mathematically confirming that being female was the most decisive determinant of survival. Furthermore, Passenger_Class exhibits significant negative correlation with survival (r = -0.33) and ticket fare (r = -0.56), verifying that higher socioeconomic class (lower class number 1) was strongly correlated with survival."
        }
    ]

    for item in visuals_info:
        # Title
        p_title = doc.add_paragraph()
        p_title.paragraph_format.space_before = Pt(14)
        p_title.paragraph_format.space_after = Pt(2)
        r_t = p_title.add_run(f"5.{item['num']} {item['title']}")
        r_t.font.size = Pt(12.5)
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_PRIMARY

        # Type badge
        p_type = doc.add_paragraph()
        p_type.paragraph_format.space_before = Pt(0)
        p_type.paragraph_format.space_after = Pt(6)
        r_typ = p_type.add_run(f"Visualization Category: {item['type']}")
        r_typ.font.size = Pt(10)
        r_typ.font.italic = True
        r_typ.font.color.rgb = COLOR_SECONDARY

        # Embed Image
        if os.path.exists(item['image']):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(4)
            p_img.paragraph_format.space_after = Pt(6)
            doc.add_picture(item['image'], width=Inches(5.7))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Explanatory Box / Paragraphs
        p_desc = doc.add_paragraph()
        p_desc.paragraph_format.space_before = Pt(4)
        p_desc.paragraph_format.space_after = Pt(3)
        r_s_lbl = p_desc.add_run("• What the Visualization Shows: ")
        r_s_lbl.font.bold = True
        r_s_lbl.font.size = Pt(10)
        r_s_txt = p_desc.add_run(item['shows'])
        r_s_txt.font.size = Pt(10)

        p_obs = doc.add_paragraph()
        p_obs.paragraph_format.space_before = Pt(2)
        p_obs.paragraph_format.space_after = Pt(12)
        r_o_lbl = p_obs.add_run("• Key Analytical Observation: ")
        r_o_lbl.font.bold = True
        r_o_lbl.font.size = Pt(10)
        r_o_txt = p_obs.add_run(item['observation'])
        r_o_txt.font.size = Pt(10)

    # -------------------------------------------------------------
    # SECTION 6: Conclusion
    # -------------------------------------------------------------
    h6 = doc.add_paragraph()
    h6.paragraph_format.space_before = Pt(16)
    h6.paragraph_format.space_after = Pt(4)
    h6_run = h6.add_run("6. Conclusion and Key Takeaways")
    h6_run.font.size = Pt(15)
    h6_run.font.bold = True
    h6_run.font.color.rgb = COLOR_PRIMARY

    p_conc = doc.add_paragraph()
    p_conc.add_run(
        "Through this assignment, we executed the foundational stages of the Data Mining workflow:\n"
        "1. Real-World Data Preprocessing: Effectively handled complex missing data patterns using domain-appropriate group median and mode imputation rather than crude mean replacement. Eliminated severe noise by pruning heavily sparse columns (>77% missing) and removing 118 duplicate rows.\n"
        "2. Feature Transformation: Standardized nomenclature, converted boolean and float attributes to clean integers, and encoded categorical attributes into numerical formats suitable for mathematical and machine learning algorithms.\n"
        "3. Precise Data Selection: Clarified the crucial difference between label-based indexing (loc[]) and position-based indexing (iloc[]) when working with non-consecutive numerical index labels.\n"
        "4. Exploratory Visualization: Applied five distinct visual methodologies to demonstrate that passenger survival was heavily governed by gender ('women and children first') and socioeconomic tier (first-class ticket status).\n\n"
        "Both required deliverables (the executed Jupyter Notebook 'Assignment1_Data_Mining.ipynb' and this Word Report 'Assignment1_Data_Mining_Report.docx') have been compiled and verified in accordance with all instructions."
    )

    doc.save("Assignment1_Data_Mining_Report.docx")
    print("Report saved successfully as 'Assignment1_Data_Mining_Report.docx'!")

if __name__ == "__main__":
    build_report()

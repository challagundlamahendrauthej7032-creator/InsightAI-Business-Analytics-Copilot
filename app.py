
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(
    page_title="InsightAI Business Analytics Copilot",
    page_icon="📊",
    layout="wide"
)

st.title("📊 InsightAI - Business Analytics Copilot")
st.caption("Upload business data, discover insights, and make better decisions.")

uploaded_file = st.file_uploader(
    "Upload your business dataset",
    type=["csv", "xlsx"]
)

if uploaded_file is None:
    st.info("Upload a CSV or Excel file to start your analysis.")
    st.stop()

try:
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    if df.empty:
        st.error("The uploaded dataset is empty.")
        st.stop()

    st.success("Dataset uploaded successfully!")

    # BUSINESS OVERVIEW
    st.header("📌 Business Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Rows", f"{len(df):,}")
    c2.metric("Total Columns", f"{len(df.columns):,}")
    c3.metric("Missing Values", f"{int(df.isna().sum().sum()):,}")
    c4.metric("Duplicate Rows", f"{int(df.duplicated().sum()):,}")

    # DATA PREVIEW
    st.header("🔍 Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

    # COLUMN INFORMATION
    st.header("📋 Column Information")
    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isna().sum().values
    })
    st.dataframe(column_info, use_container_width=True)

    # DATA QUALITY
    st.header("🧹 Data Quality Report")

    quality = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isna().sum().values,
        "Missing Percentage": (
            df.isna().mean().values * 100
        ).round(2)
    })

    st.dataframe(quality, use_container_width=True)

    st.download_button(
        "⬇️ Download Data Quality Report",
        quality.to_csv(index=False).encode("utf-8"),
        "insightai_data_quality_report.csv",
        "text/csv"
    )

    # AUTOMATIC BUSINESS INSIGHTS
    st.header("💡 Automatic Business Insights")

    sales_col = "Sales" if "Sales" in df.columns else None
    quantity_col = "Quantity" if "Quantity" in df.columns else None
    invoice_col = "InvoiceNo" if "InvoiceNo" in df.columns else None
    customer_col = "CustomerID" if "CustomerID" in df.columns else None
    country_col = "Country" if "Country" in df.columns else None
    product_col = (
        "Description" if "Description" in df.columns
        else "StockCode" if "StockCode" in df.columns
        else None
    )

    if sales_col:
        sales = pd.to_numeric(df[sales_col], errors="coerce")
        st.subheader("Business Performance")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Sales", f"{sales.sum():,.2f}")
        m2.metric("Average Sales per Row", f"{sales.mean():,.2f}")

        if invoice_col:
            orders = df[invoice_col].nunique()
            m3.metric("Unique Invoices", f"{orders:,}")
        else:
            m3.metric("Unique Invoices", "Not available")

        if customer_col:
            customers = df[customer_col].nunique()
            m4.metric("Unique Customers", f"{customers:,}")
        else:
            m4.metric("Unique Customers", "Not available")

        if quantity_col:
            quantity = pd.to_numeric(df[quantity_col], errors="coerce")
            st.metric("Total Quantity", f"{quantity.sum():,.0f}")

        if product_col:
            st.subheader("🏆 Best-Selling Product")

            product_sales = pd.DataFrame({
                "Product": df[product_col].fillna("Unknown"),
                "Sales": sales
            })
            product_sales = product_sales.dropna(subset=["Sales"])
            product_sales = (
                product_sales.groupby("Product", as_index=False)["Sales"]
                .sum()
                .sort_values("Sales", ascending=False)
            )

            if not product_sales.empty:
                best = product_sales.iloc[0]
                st.success(
                    f"Top product by sales: {best['Product']} "
                    f"— {best['Sales']:,.2f}"
                )

                st.plotly_chart(
                    px.bar(
                        product_sales.head(10).sort_values("Sales"),
                        x="Sales",
                        y="Product",
                        orientation="h",
                        title="Top 10 Products by Sales"
                    ),
                    use_container_width=True
                )

        if country_col:
            st.subheader("🌍 Country Performance")

            country_sales = pd.DataFrame({
                "Country": df[country_col].fillna("Unknown"),
                "Sales": sales
            })
            country_sales = (
                country_sales.groupby("Country", as_index=False)["Sales"]
                .sum()
                .sort_values("Sales", ascending=False)
            )

            if not country_sales.empty:
                top_country = country_sales.iloc[0]
                st.success(
                    f"Top country by sales: {top_country['Country']} "
                    f"— {top_country['Sales']:,.2f}"
                )

                st.plotly_chart(
                    px.bar(
                        country_sales.head(10).sort_values("Sales"),
                        x="Sales",
                        y="Country",
                        orientation="h",
                        title="Top 10 Countries by Sales"
                    ),
                    use_container_width=True
                )

        st.info(
            "Business recommendation: Review your highest-performing "
            "products and markets, then compare their sales and quantities "
            "to identify opportunities for growth."
        )

    else:
        st.warning(
            "No column named 'Sales' was found. "
            "General dataset analysis is available below."
        )

    # INTERACTIVE CHARTS
    st.header("📈 Interactive Business Charts")

    excluded = {"InvoiceNo", "CustomerID"}
    numeric_cols = [
        col for col in df.select_dtypes(include="number").columns
        if col not in excluded
    ]
    category_cols = df.select_dtypes(
        include=["object", "category", "string"]
    ).columns.tolist()

    if numeric_cols:
        metric = st.selectbox("Choose a metric", numeric_cols)
        chart_type = st.radio(
            "Choose chart type",
            ["Bar Chart", "Histogram", "Line Chart"],
            horizontal=True
        )

        if chart_type == "Bar Chart" and category_cols:
            category = st.selectbox(
                "Group by category",
                category_cols,
                key="general_category"
            )
            grouped = (
                df.groupby(category, dropna=False, observed=True)[metric]
                .sum()
                .reset_index()
                .sort_values(metric, ascending=False)
                .head(15)
            )
            fig = px.bar(
                grouped,
                x=category,
                y=metric,
                title=f"{metric} by {category}"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Histogram":
            fig = px.histogram(df, x=metric, title=f"{metric} Distribution")
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Line Chart":
            fig = px.line(
                df.head(1000),
                y=metric,
                title=f"{metric} — First 1,000 Rows"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Bar Chart":
            st.info("No text category columns are available.")

        st.header("📊 Numeric Summary")
        summary = df[numeric_cols].describe().T.round(2)
        st.dataframe(summary, use_container_width=True)

        st.download_button(
            "⬇️ Download Numeric Summary",
            summary.to_csv().encode("utf-8"),
            "insightai_numeric_summary.csv",
            "text/csv"
        )
    else:
        st.info("No suitable numeric columns were found for charts.")

    # DOWNLOAD DATA
    st.header("📥 Download Dataset")

    if uploaded_file.name.lower().endswith(".csv"):
        st.download_button(
            "Download CSV Copy",
            df.to_csv(index=False).encode("utf-8"),
            "insightai_dataset_copy.csv",
            "text/csv"
        )
    else:
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Dataset")

        st.download_button(
            "Download Excel Copy",
            buffer.getvalue(),
            "insightai_dataset_copy.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

except Exception as error:
    st.error(f"Unable to analyze the dataset: {error}")

st.divider()
st.caption("InsightAI | Business Analytics Copilot")

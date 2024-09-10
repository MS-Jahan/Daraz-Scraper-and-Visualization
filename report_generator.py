import os
from datetime import datetime

def generate_report(desc_stats, price_stats, price_ranges, avg_discount, max_discount_products, 
                    avg_rating, rating_dist, location_counts, correlations, visualizations):
    """
    Generates an HTML report with analysis results and visualizations.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Daraz Product Analysis Report</title>
        <style>
            body {{font-family: sans-serif;}}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
            img {{ max-width: 100%; height: auto; }}
        </style>
    </head>
    <body>
        <h1>Daraz Product Analysis Report</h1>

        <h2>Descriptive Statistics</h2>
        {desc_stats_table}

        <h2>Price Analysis</h2>
        {price_stats_table}
        {price_ranges_table}
        {price_histogram}

        <h2>Discount Analysis</h2>
        <p>Average Discount: {avg_discount:.2f}%</p>
        {max_discount_products_table}
        {discount_histogram}

        <h2>Rating and Review Analysis</h2>
        <p>Average Rating: {avg_rating:.2f}</p>
        {rating_distribution_table}
        {rating_histogram}

        <h2>Location Analysis</h2>
        {location_counts_table}
        {location_bar_chart}
        {location_price_boxplot}

        <h2>Correlation Analysis</h2>
        {correlations_table}

        <h2>Price vs. Discount</h2>
        {price_discount_scatter}

        <h2>Rating vs. Number of Reviews</h2>
        {rating_reviews_scatter}

    </body>
    </html>
    """


    # Format data for HTML tables
    desc_stats_table = desc_stats.to_html()
    price_stats_table = price_stats.to_frame().to_html()
    price_ranges_table = price_ranges.to_frame().to_html()
    max_discount_products_table = max_discount_products.to_html()
    rating_distribution_table = rating_dist.to_frame().to_html()
    location_counts_table = location_counts.to_frame().to_html()
    correlations_table = correlations.to_html()

    # Replace placeholders with formatted data and visualizations
    html_content = html_content.format(
        desc_stats_table=desc_stats_table,
        price_stats_table=price_stats_table,
        price_ranges_table=price_ranges_table,
        avg_discount=avg_discount,
        max_discount_products_table=max_discount_products_table,
        avg_rating=avg_rating,
        rating_distribution_table=rating_distribution_table,
        location_counts_table=location_counts_table,
        correlations_table=correlations_table,
        price_histogram=visualizations['price_histogram'],
        discount_histogram=visualizations['discount_histogram'],
        rating_histogram=visualizations['rating_histogram'],
        price_discount_scatter=visualizations['price_discount_scatter'],
        rating_reviews_scatter=visualizations['rating_reviews_scatter'],
        location_bar_chart=visualizations['location_bar_chart'],
        location_price_boxplot=visualizations['location_price_boxplot']
    )

    # Save the HTML report
    file_name = f"output/daraz_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(file_name, "w") as f:
        f.write(html_content)

    return file_name
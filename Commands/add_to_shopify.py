import base64
import requests
import json

shared_code_file = "./shared_code.py"
with open(shared_code_file) as file:
    exec(file.read())
operation_name = "add_to_shopify"

html_template_file = os.path.join(template_dir, "shopify_profile.html")
api_key='6ae5f1a8049eb87f1a430722b37bbc35'
api_password = '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'
hostname = 'timeless-gallery-antique.myshopify.com'
version = '2021-01'
auth = f'{api_key}:{api_password}'
b64_auth = base64.b64encode(auth.encode()).decode("utf-8")
headers = {
    "Authorization": f"Basic {b64_auth}",
    "Content-Type": "application/json" 
}


def execute_operation():
    item_id = sys.argv[1]
    item_image_dir = os.path.join(imagebase_dir, item_id)

    load_db_entry_to_global(item_id)

    global age_class
    age_class = "" if age_class == "contemporary" else age_class

    shopify_images = []
    for image_name in os.listdir(item_image_dir):
        with open(os.path.join(item_image_dir, image_name), "rb") as file:
            binary = file.read()
        base64_binary = base64.b64encode(binary).decode()
        image_file_name = f"{catalogue_number},{item_name}_{image_name.split('_')[1]}"
        image_object = {
            "attachment": f"{base64_binary}\n",
            "filename": image_file_name
        }
        shopify_images.append(image_object)

    title_highlight = f"{short_highlight} -" if short_highlight != "" else ""
    shopify_title = f"{catalogue_number} {item_name} - {title_highlight} {age_class} Porcelain Figurine by {manufacturer}, {period} (Item# {item_id})"
    seo_title = f"{catalogue_number} - {item_name} - {age_class} Royal Doulton Figurine"
    seo_description = f"A {age_class} Royal Doulton HN Series porcelain figurine, {period}. The figurine is numbered {catalogue_number} with the name “{item_name}”, in the “{series}” Series. The figurine is hand made and hand decorated. This is a {collection_class} Royal Doulton collectable piece."

# ref: https://shopify.dev/docs/admin-api/rest/reference/products/product
    shopify_item_json = {
        "product": {
            "title": shopify_title,
            "status": "active",
            "vendor": manufacturer,
            "product_type": "Figurine",
            "body_html": generate_html(),
            "images": shopify_images,
            "variants": [{
                "price": pricing,
                "cost": total_cost,
                "sku": item_id,
                "taxable": False
            }],
            "handle": item_id,
            "metafields_global_title_tag": seo_title,
            "metafields_global_description_tag": seo_description
        }
    }
    response = requests.post(
        url=f"https://{hostname}/admin/api/{version}/products.json",
        headers=headers,
        data=json.dumps(shopify_item_json)
    )
    print(response)


def generate_html():
    with open(html_template_file, 'r') as file:
        html = file.read()
    html = html.replace("{{age_class}}", age_class)
    html = html.replace("{{period}}", period)
    html = html.replace("{{catalogue_number}}", catalogue_number)
    html = html.replace("{{item_name}}", item_name)
    html = html.replace("{{series}}", series)
    html = html.replace("{{collection_class}}", collection_class)
    html = html.replace("{{model_start_year}}", str(model_start_year))
    html = html.replace("{{model_end_year}}", str(model_end_year))
    html = html.replace("{{artist}}", artist)
    html = html.replace("{{height}}", str(height))
    html = html.replace("{{height_cm}}", "%.2f" % (float(height)*2.54))
    html = html.replace("{{condition}}", generate_condition_verbiage())
    return html


def generate_condition_verbiage():
    if condition == "Perfect" or condition == "perfect":
        return "in perfect vintage condition, no chips or crackings"
    elif condition == "Great" or condition == "great":
        return "in great vintage condition"
    elif condition == "Good" or condition == "good":
        return "overall in good vintage condition"
    elif condition == "Fair" or condition == "fair":
        return "overall in good vintage condition, but has some minor imperfection"
    else:
        return condition


if __name__ == "__main__":
    assert len(sys.argv) == 2, f"incorrect number of arguments: need 1, actual {len(sys.argv) - 1}"
    execute_operation()

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import pdfkit
import yaml

TEMPLATES = [
    "template.html",
    "template_moderne.html",
    "template_editorial.html",
    "template_compact.html",
]


def generate_cv(templates: list[str] | None = None) -> list[Path]:
    template_list = templates if templates is not None else TEMPLATES

    # 1. Charger les données YAML
    with open("cv_data.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # 2. Configurer Jinja2 et wkhtmltopdf
    env = Environment(loader=FileSystemLoader("."))
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {"encoding": "UTF-8"}

    base_name = data["infos"]["nom"].replace(" ", "_")
    generated_files: list[Path] = []

    # 3. Générer un PDF par template
    for template_name in template_list:
        template = env.get_template(template_name)
        html_out = template.render(cv=data)

        variant = Path(template_name).stem
        output_pdf = Path(f"CV_{base_name}_{variant}.pdf")

        pdfkit.from_string(html_out, str(output_pdf), configuration=config, options=options)
        generated_files.append(output_pdf)
        print(f"CV généré avec succès : {output_pdf}")

    return generated_files


if __name__ == "__main__":
    generate_cv()
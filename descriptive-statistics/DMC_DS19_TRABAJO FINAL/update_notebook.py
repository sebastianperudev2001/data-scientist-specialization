
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
notebook_path = os.path.join(script_dir, 'CHAVARRY_EF.ipynb')

# 1. Read Notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# 2. Define New Cells
markdown_cell = {
    "cell_type": "markdown",
    "id": "feature_eng_md",
    "metadata": {},
    "source": [
        "## 4. Generación de Nueva Variable: Tipo de Seguro\n",
        "A partir de las variables `P4191` a `P4198`, crearemos una nueva variable numérica `TIPO_SEGURO` para clasificar el tipo de cobertura de cada persona.\n",
        "\n",
        "**Codificación (con jerarquía de prioridad):**\n",
        "*   **4**: Privado / EPS / Universitario / Escolar (Prioridad Alta)\n",
        "*   **3**: Fuerzas Armadas / Policiales\n",
        "*   **2**: EsSalud\n",
        "*   **1**: SIS (Seguro Integral de Salud)\n",
        "*   **5**: Otro\n",
        "*   **0**: Ninguno\n"
    ]
}

code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "id": "feature_eng_seguro",
    "metadata": {},
    "outputs": [],
    "source": [
        "# Definimos la función de clasificación\n",
        "def clasificar_seguro(row):\n",
        "    # Función auxiliar para verificar si tiene el seguro (ignora 'No' y nulos)\n",
        "    def has(col):\n",
        "        val = row[col]\n",
        "        # Verificamos que no sea nulo y que no sea la cadena 'No'\n",
        "        if pd.isna(val) or val == 'No':\n",
        "            return False\n",
        "        return True\n",
        "\n",
        "    # Prioridad 4: Privados y otros\n",
        "    if has('P4192') or has('P4193') or has('P4196') or has('P4197'):\n",
        "        return 4\n",
        "    # Prioridad 3: FF.AA / Policiales\n",
        "    if has('P4194'):\n",
        "        return 3\n",
        "    # Prioridad 2: EsSalud\n",
        "    if has('P4191'):\n",
        "        return 2\n",
        "    # Prioridad 1: SIS\n",
        "    if has('P4195'):\n",
        "        return 1\n",
        "    # Prioridad 5: Otro\n",
        "    if has('P4198'):\n",
        "        return 5\n",
        "        \n",
        "    # Caso 0: Ninguno\n",
        "    return 0\n",
        "\n",
        "# Aplicamos la transformación\n",
        "print(\"Generando nueva variable 'TIPO_SEGURO'...\")\n",
        "df_eda['TIPO_SEGURO'] = df_eda.apply(clasificar_seguro, axis=1)\n",
        "\n",
        "# Visualizamos los resultados\n",
        "print(\"Conteo por Tipo de Seguro:\")\n",
        "counts = df_eda['TIPO_SEGURO'].value_counts().sort_index()\n",
        "print(counts)\n",
        "\n",
        "# Opcional: Crear etiqueta para validación visual\n",
        "labels = {0: 'Ninguno', 1: 'SIS', 2: 'EsSalud', 3: 'FFAA', 4: 'Privado', 5: 'Otro'}\n",
        "print(\"\\nDistribución con etiquetas:\")\n",
        "print(counts.rename(index=labels))"
    ]
}

# 3. Append Cells
print("Appending cells...")
nb['cells'].append(markdown_cell)
nb['cells'].append(code_cell)

# 4. Save Notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook updated successfully.")

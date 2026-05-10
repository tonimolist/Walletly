# back-office-domain

### Estructura del Projecte


**Configuració i Seguretat**

* **.env**: El caixa fort amb les dades sensibles i contrasenyes.
* **config.py**: El selector que agafa les dades del caixa fort segons l'entorn.
* **pyproject.toml**: El DNI i la llista de la compra general del projecte.
* **requirements.txt**: La llista detallada amb les versions exactes de cada llibreria.


**Cor de l'Aplicació (domain)**

* **db.py**: El motor que obre la canonada cap a la base de dades.
* **models.py**: El plànol que defineix les taules i les seves relacions.
* **__init__.py**: L'empaquetador que ho lliga tot per facilitar-ne l'ús.


**Execució i Anàlisi (Notebooks)**

* **000_Environment.ipynb**: El banc de proves per verificar que tot estigui ben instal·lat.
* **010_Models_Creation.ipynb**: El taller on es creen les taules i es proven els models.
* **020_Analysis.ipynb**: El laboratori per fer consultes i informes de dades.
* **030_Models_Create_v2.ipynb**: La versió evolucionada del taller amb retocs de disseny.


**Documentació i Dades**

* **ERD_Walletly.pdf**: El mapa visual que ensenya com es connecten totes les taules.
* **back-office-structure.pdf**: La guia d'organització interna de l'aplicació.
* **walletly.db**: La caixa real on es guarden físicament tots els teus moviments.
* **README.md**: La guia ràpida per entendre què fa cada peça del projecte.
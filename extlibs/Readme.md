# Préparer Zlib pour Windows

Suivre les étapes suivantes **uniquement** si ce que j'ai mis dans le repo n'est pas suffisant chez vous.

1. Télécharger le code source de Zlib 1.2.11 ici : https://zlib.net/zlib1211.zip.
2. Ouvrir le fichier `zlib-1.2.11/contrib/vstudio/vc14/zlibvc.sln` (ça ouvre Visual Studio)
3. Configurer en **Release** pour **x64**
4. Tout build
5. Récupérer les 2 fichiers `./x64/ZlibStatRelease/` en `.lib` et en `.pdb` et les mettre dans ce dossier dans `zlib/lib`. 
6. Renommer **`zlibstat.lib`** en **`zlibstatic.lib`**.
7. Copier-coller tous les fichiers header (en `.h`) dans le dossier des sources de Zlib et les mettre dans ce dossier dans `zlib/include`. 

Normalement ça suffit. 

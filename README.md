# Mini-Aevol-Hypervitesse : A mini-application based on the Aevol simulator

Projet OT5 de Félix CASTILLON, Martin FRANCESCHI, David HAMIDOVIC, Ousmane TOUAT

Pour plus de détails, voir notre rendu PDF.

## Branches

* `master` : version originale du projet.
* `master-nostdout` : version originale où on a simplement désactivé les affichages dans stdout pour le cas d'usage général. 
* `ma1` : version avec les améliorations. 
   * Les traces et OpenMP s'activent via les options CMake.
   * Les optimisations diverses s'activent dans le CMakeLists.txt. 
    
## Divers

La mise en compatibilité pour que le projet compile sous Windows est dans le dossier `include_helpers`.

Les outils Python sont dans le dossier `Benchmarking`. 

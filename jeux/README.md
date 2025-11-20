# 🎮 Last Wave  
Petit jeu vidéo réalisé en Python (Pygame) respectant les mécaniques imposées du projet.

## 📝 Description
**Last Wave** est un mini-jeu d’action en vue du dessus où le joueur doit survivre à plusieurs vagues d’ennemis avant d’affronter un **boss final**.  
Le gameplay met l’accent sur une **ressource limitée (munitions)**, une **boucle de progression**, et une confrontation finale.

Ce projet respecte **toutes les règles imposées** et peut être lancé facilement en une seule commande.

---

## ✔️ Fonctionnalités obligatoires

- **1 Boss final**  
- **2 types d’ennemis**  
  - *Chaser* : poursuit le joueur  
  - *Patrol* : patrouille horizontalement  
- **1 ressource limitée : munitions**  
  - Stock initial limité  
  - Pickups de recharge aléatoires  
- **1 boucle de progression (vagues)**  
  - Vague 1 → Vague 2 → Vague 3 → Boss  
- **Écran de Game Over + Restart**  
  - Appuyer sur **R** pour recommencer  
- **Stabilité & Performance**  
  - Aucun crash, FPS stable (~60)

---

## 🕹️ Contrôles

| Action | Touche |
|-------|--------|
| Déplacer le joueur | ZQSD ou Flèches |
| Tirer | Clic gauche |
| Redémarrer après Game Over | R |

---

## 🎯 Objectif du jeu
- Survivre aux vagues croissantes d’ennemis  
- Gérer ses **munitions limitées**  
- Battre le **boss** pour remporter la partie

---

## 💡 Mécaniques détaillées

### 🟦 Joueur
- Déplacement fluide en 8 directions  
- Tir dirigé avec la souris  
- Stock de munitions limité  
- Recharge via pickups

### 🔻 Ennemis
#### 1. **Chaser Enemy**
- Se dirige en permanence vers le jou

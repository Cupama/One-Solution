# Cupama Site Visit Sheet — Module Odoo 16

> Module développé pour **Cupama Ltd** — Gestion des fiches de visite de site pour l'installation de revêtements de sol SPC.

---

## 📋 Description

Ce module ajoute un système complet de **fiches de visite de site** (Site Visit Sheet) directement intégré au flux de vente Odoo. Il permet aux techniciens de documenter l'état des lieux avant l'installation de revêtements SPC : accessibilité, état du sol, dimensions des pièces, conditions client et signature.

Un **smart button** est ajouté sur chaque devis/commande pour créer ou accéder rapidement à la fiche de visite correspondante.

---

## ✅ Fonctionnalités

- **Fiche de visite complète** reflétant le formulaire papier Cupama :
  - Informations client (nom, tél, adresse)
  - Niveau d'étage et statut de la maison
  - Checklist état des lieux (accès, objets lourds, point électrique, livraison, dépose carrelage)
  - Statut de la surface (carrelage, incomplet, poli)
  - Accessoires : Skirting, Bar T Reducer
  - Photos du site (pièces jointes)
  - Tableau des dimensions par pièce avec calcul automatique de surface (m²)
  - Conditions d'installation avec signature électronique du client
  - Remarques additionnelles

- **Smart button** sur le devis et la commande de vente :
  - Crée une nouvelle fiche (avec pré-remplissage client/adresse/tél)
  - Accède à la fiche existante en un clic
  - Compteur visible du nombre de visites liées

- **Workflow** : Brouillon → Confirmé → Terminé / Annulé
- **Numérotation automatique** : `SVS/2026/0001`
- **Chatter** (messages, activités, suivi)
- **Vues** : formulaire, liste, recherche avec filtres et regroupements

---

## 🔧 Prérequis

| Élément | Version |
|---|---|
| Odoo | **16.0** |
| Module dépendant | `sale_management` |
| Python | 3.10+ |
| PostgreSQL | 12+ |

---

## 🚀 Installation

### Méthode 1 — Via le dossier addons (recommandée)

1. **Télécharger et décompresser** le fichier `cupama_site_visit.zip` :
   ```bash
   unzip cupama_site_visit.zip -d /path/to/odoo/addons/
   ```

2. **Vérifier la structure** du dossier décompressé :
   ```
   addons/
   └── cupama_site_visit/
       ├── __manifest__.py
       ├── __init__.py
       ├── models/
       │   ├── __init__.py
       │   ├── site_visit_sheet.py
       │   └── sale_order.py
       ├── views/
       │   ├── site_visit_sheet_views.xml
       │   └── sale_order_views.xml
       └── security/
           └── ir.model.access.csv
   ```

3. **Redémarrer le serveur Odoo** :
   ```bash
   # Systemd
   sudo systemctl restart odoo

   # Ou directement
   ./odoo-bin -c /etc/odoo/odoo.conf --stop-after-init
   ./odoo-bin -c /etc/odoo/odoo.conf
   ```

4. **Activer le mode développeur** dans Odoo :
   - Aller dans **Paramètres → Technique → Activer le mode développeur**
   - Ou ajouter `?debug=1` à l'URL

5. **Mettre à jour la liste des applications** :
   - Aller dans **Applications → Mettre à jour la liste des Apps**

6. **Installer le module** :
   - Chercher `Cupama Site Visit Sheet` dans la liste des applications
   - Cliquer sur **Installer**

---

### Méthode 2 — Via la ligne de commande (installation directe)

```bash
./odoo-bin -c /etc/odoo/odoo.conf \
  -d NOM_DE_VOTRE_BASE \
  -i cupama_site_visit \
  --stop-after-init
```

---

### Méthode 3 — Via Docker

```bash
# Copier le module dans le conteneur
docker cp cupama_site_visit/ <container_id>:/mnt/extra-addons/

# Redémarrer le conteneur
docker restart <container_id>

# Puis installer via l'interface ou CLI :
docker exec <container_id> odoo -d NOM_BASE -i cupama_site_visit --stop-after-init
```

---

## 📖 Utilisation

### Créer une fiche de visite depuis un devis

1. Ouvrir un **Devis** ou une **Commande de vente** dans le module Ventes
2. Cliquer sur le **smart button** `📍 New Site Visit` (visible si aucune fiche n'existe encore)
3. La fiche est créée automatiquement avec les informations du client pré-remplies
4. Compléter les champs de la fiche : checklist, dimensions, photos, signature
5. Cliquer sur **Confirmer** puis **Marquer comme Terminé** une fois la visite effectuée

### Accéder aux fiches existantes

- Depuis la commande : cliquer sur le smart button `📍 Site Visits (N)`
- Depuis le menu : **Ventes → Site Visits → Site Visit Sheets**

### Accès par rôles

| Rôle | Lecture | Écriture | Création | Suppression |
|---|---|---|---|---|
| Commercial (Salesman) | ✅ | ✅ | ✅ | ❌ |
| Responsable des ventes | ✅ | ✅ | ✅ | ✅ |

---

## 🗂️ Structure technique

```
cupama_site_visit/
│
├── __manifest__.py              # Déclaration du module (v16.0)
├── __init__.py
│
├── models/
│   ├── __init__.py
│   ├── site_visit_sheet.py      # Modèle cupama.site.visit.sheet
│   │                            # + cupama.site.visit.dimension
│   └── sale_order.py            # Extension sale.order (smart button)
│
├── views/
│   ├── site_visit_sheet_views.xml   # Form, Tree, Search, Menu, Séquence
│   └── sale_order_views.xml         # Injection du smart button
│
└── security/
    └── ir.model.access.csv      # Droits d'accès
```

**Modèles créés :**
- `cupama.site.visit.sheet` — Fiche de visite principale
- `cupama.site.visit.dimension` — Lignes de dimensions (One2many)

---

## 🔄 Mise à jour du module

```bash
./odoo-bin -c /etc/odoo/odoo.conf \
  -d NOM_DE_VOTRE_BASE \
  -u cupama_site_visit \
  --stop-after-init
```

---

## 🐛 Dépannage

| Problème | Solution |
|---|---|
| Module non visible dans la liste | Vérifier le chemin addons dans `odoo.conf` (`addons_path`) et mettre à jour la liste |
| Erreur de droits d'accès | Vérifier que `sale_management` est bien installé |
| Smart button absent | Vider le cache navigateur + redémarrer Odoo |
| Erreur de séquence | Aller dans **Paramètres → Technique → Séquences** et vérifier `SVS/` |

---

## 📞 Support

**Cupama Ltd** — Module interne  
Version : `16.0.1.0.0`  
Licence : LGPL-3

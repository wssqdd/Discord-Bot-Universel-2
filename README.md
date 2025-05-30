
# Bot Discord - Gestion, Fun et Modération

Bienvenue sur le dépôt GitHub de ce **bot Discord polyvalent**. Il permet une gestion simple des utilisateurs, offre des fonctionnalités ludiques et propose des outils de modération avancés pour les administrateurs de serveurs.

## Fonctionnalités

### Commandes Utilisateurs

| Commande | Description |
|---------|-------------|
| `!fiche` | Affiche les fiches disponibles. |
| `!level` | Affiche votre niveau actuel. |
| `!xp` | Affiche votre quantité d'XP actuelle. |
| `!leaderboard_xp` | Affiche le classement basé sur l'XP. |
| `!leaderboard_level` | Affiche le classement basé sur les niveaux. |
| `!suggest` | Permet de faire une suggestion. |
| `!hangman` | Lance une partie du jeu du pendu. |
| `!8ball` | Pose une question au bot et obtient une réponse aléatoire. |
| `!help` | Affiche cette liste de commandes. |

### Commandes Admin / Modération

| Commande | Description |
|---------|-------------|
| `!antibot` | Active ou désactive la protection contre les bots. |
| `!antiinvitation` | Active ou désactive la détection d'invitations. |
| `!antilien` | Active ou désactive la détection de liens. |
| `!antimajuscule` | Active ou désactive le filtre de majuscules. |
| `!antispam` | Active ou désactive l'anti-spam. |
| `!bl` | Ajoute un membre à la liste noire. |
| `!unbl` | Retire un membre de la liste noire. |
| `!listbl` | Affiche la liste des membres blacklistés. |
| `!addfiche` | Ajoute une nouvelle fiche. |
| `!setup_ticket` | Configure le système de ticket. |
| `!prefix` | Change le préfixe du bot. |
| `!vid` | Publie une vidéo (fonction personnalisée). |
| `!mute` | Réduit un membre au silence. |
| `!unwarn` | Supprime un avertissement d’un membre. |
| `!listwarn` | Affiche les avertissements d’un membre. |
| `!givepoint` | Donne des points à un membre. |
| `!removepoint` | Retire des points à un membre. |
| `!help_admin` | Affiche cette liste de commandes admin. |

## Configuration

Le préfixe du bot est stocké dynamiquement dans un fichier `config.json`. Exemple de structure :

```json
{
  "prefix": "!",
  "color_embed": 123456
}
````

## Installation

1. Clonez ce dépôt :

   ```bash
   git clone https://github.com/votre-utilisateur/nom-du-bot.git
   ```
2. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```
3. Créez un fichier `config.json` avec votre préfixe et la couleur des embeds.
4. Lancez le bot :

   ```bash
   python bot.py
   ```

## Auteurs

* Développé par 1901 (wssqdd)
* Rejoignez notre serveur Discord pour le support et les mises à jour

## Licence

Ce projet est sous licence MIT. Vous êtes libre de le modifier et de le redistribuer.


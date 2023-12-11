# [Connect Four](https://ci-pp3-connect-four-8982dfb728aa.herokuapp.com/)

Connect Four is an interactive Python game that combines the classic strategy of Connect Four with modern programming techniques.
The game supports both single-player (against a computer opponent) and two-player modes.

![Mockup-connect-four](https://github.com/GKopanidis/ci-pp3-connect-four/assets/145017421/9f8f1d9a-4087-49b2-ae09-2577b3a9ddca)

[Connect-Four live site](https://ci-pp3-connect-four-8982dfb728aa.herokuapp.com/)

## [Index - Table of Contents](#index-table-of-contents)

- [Introduction](#Introduction)
   - [Target Audience](#Target-Audience)
   - [Site Goals](#Site-Goals)

- [Overview](#overview)
  - [Features](#features)
  - [Existing Features](#existing-features)
  - [Features Planned](#features-planned)

- [Technolgies](#technologies)

- [Logical Flow](#logical-flow)

- [Testing](#testing)

   - [Pep8 Validation](#pep8-validation)
   - [Light House Report](#light-house-report)
   - [Tested Browser](#tested-browser)
   - [Manual Testing](#manual-testing)
   - [Fixed Bugs](#fixed-bugs)
   - [Unfixed Bugs](#unfixed-bugs)

- [Deployment](#deployment)
   - [Version Control](#version-control)
   - [Deployment to Github Pages](#deployment-to-github-pages)
   - [Heroku Deployment](#heroku-deployment)
   - [Clone the Repository Code Locally](#clone-locally)
      
- [Credits](#credits)

   - [Content](#content)
   - [Media](#media)
   - [Acknowledgments](#acknowledgments)
 
## Introduction

Welcome to the Connect Four Python Game, an interactive and fun adaptation of the classic two-player connection game, now available in a Python console application. This engaging project is designed for both beginners and seasoned players, offering an immersive experience in the world of text-based gaming.

[Back to Top](#Introduction)

### Target Audience

The Connect Four Python Game is designed to captivate a diverse audience, encompassing everyone from programming novices who are delving into the world of Python, to casual gamers seeking a quick and strategic challenge.

### Site Goals

As a User:

   - **Engagement and Entertainment:**
      - Fun Gameplay: Expect an enjoyable and engaging game experience, true to the essence of Connect Four.
      - User-Friendly Interface: A clear and easy-to-navigate interface that enhances the gaming experience.

   - **Challenge and Competitiveness:**
      - Challenging: For those playing against the computer, an computer that is smart enough to provide a good challenge.
      - Competitive Multiplayer: In two-player mode, an environment that fosters healthy competition.

   - **Reliability and Performance:**
      - Smooth Performance: The game should run smoothly without any significant lag or performance issues.
      - Error Handling: Minimal bugs and crashes, with proper error handling for a seamless experience.
        
   - **Accessibility and Learning:**
      - Easy to Learn: The game should be simple enough for beginners to understand and start playing quickly.
      - Educational Value: Opportunity to learn basic strategies of Connect Four for first-time players.
    
As a Creator:

   - **Technical Proficiency and Growth:**
      - Code Quality: A well-structured, readable, and maintainable codebase.
      - Skill Enhancement: Opportunity to improve Python programming skills, particularly in areas like AI logic, data handling, and UI development.
        
   - **Innovation and Creativity:**
      - Creative Freedom: The ability to implement new features or modify existing ones creatively.
      - Problem-Solving: Tackling various technical and design challenges that arise during development.
     
   - **Community Engagement and Feedback:**
      - User Feedback: Receiving constructive feedback from users to help improve the game.
      - Community Interaction: Engaging with a community of users and developers, facilitating knowledge exchange and collaboration.

   - **Personal Satisfaction and Accomplishment:**
      - Achieving Goals: Successfully bringing a game concept to life.
      - Personal Fulfillment: A sense of accomplishment from creating a game that people enjoy.
    
## Overview

### Features

The Connect Four Python Game comes equipped with a variety of features that make it both engaging and functional. Here’s an overview of the existing features you’ll find in this game:

### Existing Features

   - **Interactive Gameplay:**
      - Two Modes of Play: Players can choose to play against a computer AI for a challenging experience or opt for a two-player mode for a competitive game against a friend.
      - Dynamic Game Board: A 6x7 grid that closely replicates the traditional Connect Four game, providing a familiar yet refreshed gaming experience.

   - **User Experience:**
     - Clear Console Interface: The game boasts a user-friendly console interface, making navigation and gameplay straightforward and enjoyable.
     - Color-Coded Pieces: Different colors represent different players, enhancing the visual aspect of the game and making it easy to track moves.
       
   - **Performance and Reliability:**
     - Efficient Codebase: The game is built with efficiency in mind, ensuring smooth gameplay.
     - Error Handling: Robust error handling is in place to minimize crashes and bugs, providing a seamless gaming experience.

   - **Player Progress Tracking:**
     - Hall of Fame Integration: The game integrates with Google Sheets to record player statistics, including wins and losses, offering players a sense of progression and achievement.

   - **Educational Aspect:**
     - Code Comments and Documentation: The source code is well-documented and commented, making it an excellent resource for those looking to learn Python or understand game development basics.

   - **Customization and Expansion Potential:**
     - Modifiable Code: Players with programming knowledge can easily modify or extend the game's features, offering a customizable experience.

### Features Planned

   - **Advanced AI Decision-Making:**
      - We're working on empowering the AI to make more strategic choices, enhancing the challenge for players in single-player mode. This improvement will ensure that each game against the computer is not just engaging but also tests the player's strategic skills to the fullest.

   - **Integrated Timer Functionality:**
     - To add an element of excitement and urgency, we plan to introduce a timer feature. This will set a time limit for each player's turn, making the game more dynamic and fast-paced.

   - **Varied Game Modes: Easy and Hard:**
     - Recognizing that our players have different skill levels and preferences, we're introducing multiple game modes. An 'Easy' mode will cater to beginners or those looking for a more relaxed gameplay experience, while the 'Hard' mode will challenge seasoned players with a more sophisticated AI opponent.

## Technologies
 
   - Python ![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
      - The logic was created using Python.

   - Gitpod ![Gitpod](https://img.shields.io/badge/Gitpod-000000?style=for-the-badge&logo=gitpod&logoColor=#FFAE33)
      - The app was developed using Gitpod IDE

   - GitHub ![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
      - Source code is hosted on GitHub.

   - Git ![Git](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)
      - Used to commit and push code during the development of the Website
 
   - Heroku ![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)
     - The app was deployed using Heroku.
 
   - Shields.io
      - Shields created with [Shields.io](https://shields.io/badges/static-badge)
        and
        [more shields](https://github.com/alexandresanlim/Badges4-README.md-Profile)

## Logical Flow

<img src="https://github.com/GKopanidis/ci-pp3-connect-four/assets/145017421/b2df3cd9-2218-4b66-9a2e-d52567bc5d8d" width="50%" height="50%">

## Testing
### PEP8 Validation
   - [PEP8 validator](https://pep8ci.herokuapp.com/)
     
     <img src="https://github.com/GKopanidis/ci-pp3-connect-four/assets/145017421/972ffe37-59f0-43d4-b975-aaa0e67d8c30" width="50%" height="50%">

     **NOTE:**
         Some errors that were found and fixed included: "Trailing whitespace" and "Line too long"

### Light House Report
   - [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview?hl=en)

     <img src="https://github.com/GKopanidis/ci-pp3-connect-four/assets/145017421/8c06b31c-83db-41a9-beed-416d7ed7538d" width="50%" height="50%">

### Tested Browser
   - Latest versions:
     <table>
       <thead>
       <tr>
       <th align="center">Browser</th>
       <th align="center">Layout</th>
       <th align="center">Functionality</th>
       </tr>
       </thead>
       <tbody>
         <tr>
         <td align="center">Chrome</td>
         <td align="center">✔</td>
         <td align="center">✔</td>
         </tr>
         <tr>
         <td align="center">Edge</td>
         <td align="center">✔</td>
         <td align="center">✔</td>
         </tr>
         <tr>
         <td align="center">Firefox</td>
         <td align="center">✔</td>
         <td align="center">✔</td>
         </tr>
         <tr>
         <td align="center">Safari</td>
         <td align="center">✔</td>
         <td align="center">❌</td>
         </tr>
       </tbody>
     </table>

     **NOTE:**
         Since the template from CodeInstitute must be used, it is known that it does not work correctly for Mac/Safari and iOS/Safari.

### Manual Testing
   to be continued...

## Fixed Bugs
   - No bugs found at this time

## Unfixed Bugs
   - No bugs found at this time

## Deployment

   ### Version Control

   The site was created using the Gitpod IDE and pushed to Git Hub to the remote repository ‘ci-pp3-connect-four’.
   
   The following git commands were used throughout development to push code to the remote repo:
   
   ```git add <file>``` - This command was used to add the file(s) to the staging area before they are committed.
   
   ```git commit -m “commit message”``` - This command was used to commit changes to the local repository queue ready for the final step.
   
   ```git push``` - This command was used to push all committed code to the remote repository on Git Hub.

   ## Deployment to GitHub Pages

   To deploy this page to Heroku from its Gitpod repository, the following steps were taken:
   
   1. Get Python Essentials Template from Code Institute [P3 Template](https://github.com/Code-Institute-Org/p3-template "p3 template link")
   2. Create a new repository using the P3 template 
   3. Copy the repo URL and copy it into Gitpod to create a new workspace
   4. Close the README tab and create the first file named index.html
   5. Open the terminal, type (git add .) (git commit -m "initial commit") (git push)
   6. Type 'Pip3 freeze > requirements.txt' into the terminal and commit. 
   7. Log into [Heroku]( https://id.heroku.com/login "Link to Heroku login page") 
   8. Create a new app and name it "connect-four"
   9. Add config vars - The key is PORT and the value is 8000
   10. Add build pack, select Python - click save, then select node.js - click save - in that order
   11. Go to the deploy section - select automatic deploys (If you prefer not to have automatic deploys, you can select the 'Manual Deploy' option below)
   12. The project is now deployed.
       
   [Connect-Four live site](https://ci-pp3-connect-four-8982dfb728aa.herokuapp.com/)

   ### Heroku Deployment

   The below steps were followed to deploy this project to Heroku:

   - Go to Heroku and click "New" to create a new app.
   - Choose an app name and region region, click "Create app".
   - Go to "Settings" and navigate to Config Vars. Add the following config variables:
      - PORT : 8000
      - Navigate to Buildpacks and add buildpacks for Python and NodeJS (in that order).
   - Navigate to "Deploy". Set the deployment method to Github and enter repository name and connect.
   - Scroll down to Manual Deploy, select "main" branch and click "Deploy Branch".
   - The app will now be deployed to heroku

   [Connect-Four live site](https://ci-pp3-connect-four-8982dfb728aa.herokuapp.com/)

   ### Clone Locally

   - Open IDE of choice and type the following into the terminal:
       * ```git clone https://github.com/GKopanidis/ci-pp3-connect-four.git```
   - Project will now be cloned locally.

## Credits

## Content

Each of these tools and resources has played a significant role in shaping the Connect Four Python Game, contributing to its functionality, user experience, and overall aesthetic appeal.

[Colorama](https://pypi.org/project/colorama/ "link to colorama")
   - Colorama is an essential tool used in our game for adding color to the console output. It enhances the visual aspect of the game, making it more engaging and easier to differentiate between various elements, such as player pieces.

[Pyfiglet](https://pypi.org/project/pyfiglet/ "link to pyfiglet")
   - Pyfiglet plays a crucial role in elevating the game's interface. It is used for generating ASCII art text, which adds a visually appealing and professional touch to the game's headings and displays.

[Clear screen](https://www.geeksforgeeks.org/clear-screen-python/ "link to clear screen")
   - The Clear Screen method is integral to maintaining a clean and organized display in the console. It helps in refreshing the screen between turns or actions, ensuring a clutter-free gaming environment.

[Time](https://docs.python.org/3/library/time.html "link to time")
   - The Time module is a key component in the game. It's used for implementing delays and countdowns, enhancing the user experience by providing timely feedback and creating a more dynamic game flow.

[Love Sandwiches](https://github.com/sarahgoodwin93/love-sandwiches "link to love sandwiches")
   - Love Sandwiches was used as part of the education process and was referred back to for the deployment of the project

## Media

**Background image for Main-Page:**
   - AI image generator

### Acknowledgments

- Thank you to my mentor [Gareth-McGirr](https://github.com/Gareth-McGirr) who provided me with lots of pointers on resources to help on my 3rd project!
- Thank you to [Salko Nuhanovic](https://github.com/salkonuhannovic) who helped me on the player_move and computer_move functions!
- Thank you to Raphael Kopanidis who helped me on the classes!

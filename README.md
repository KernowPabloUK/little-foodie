# Little Foodie - Track Tiny Tastes, One Bite at a Time

A baby weaning & tracking full stack web application - Capstone Project for Code Institute

![Responsive design preview](./static/images/readme_images/responsive_site_little_foodie.png)

**Author:** Paul Morgan - calculatedCode

## Description

The purpose of this full stack web application is to allow parents and caregivers to record and monitor their babies weaning journey.
As a site owner, the site is designed to be welcoming and informative with an organised layout to assist external users' usage.

This has been built using Django, Python, JavaScript, HTML, CSS, and the Bootstrap framework and Google Fonts. Excluding items listed below (AI Usage Within the Project), all code/work is my own.
Informational sources are taken from [NHS](https://www.nhs.uk/start-for-life/baby/weaning/) and the [Food Standards Agency](https://www.food.gov.uk/food-safety-and-hygiene/food-allergies-intolerances-and-coeliac-disease)

## Features

1. Homepage (Login/Register)
2. About Little Foodie
    1. How to use the app
    2. Information & Sources
    3. Disclaimer
3. Get In Touch
    1. Error Reporting
    2. Feature Request
4. Profile Section
    1. User Profile
    2. User Children
5. Food Logs section
    1. New Food Logs
    2. Historical Food Logs
6. Stats section
    1. Food Statistics
    2. Category Statistics

## Deployment Procedure //TODO - writeup

The site will be deployed using Heroku using the following steps.

## How to View the Project

- [View the deployed website](https://little-foodie-3451586f5ac7.herokuapp.com/)

## AI Usage Within the Project //TODO - writeup

- AI used to refine user stories into tasks and acceptance criteria.
- AI used to generate all images and logo design.
- AI used to verify ERD functionality
- AI used to generate description and meta keywords for SEO within "< head >".
- AI used to create AJAX API function call for Food Log
- AI used to generate code for Graphs on statistics page
- AI used to refine unit tests
- AI used to enhance existing docstrings

## Documents

The wireframing and initial design of the website was done with a mobile first approach, especially as parents will most likely have limited time to record the food entry so a mobile phone is the most convenient manner to access Little Foodie.

Homepage
![Wireframe Design - Homepage](./static/images/readme_images/little_foodie_-_wireframe_-_homepage.png)

Profile Page
![Wireframe Design - Profile Page](./static/images/readme_images/little_foodie_-_wireframe_-_account_page.png)

Food Log Page
![Wireframe Design - Food Log Page](./static/images/readme_images/little_foodie_-_wireframe_-_log_page.png)

Stats Page
![Wireframe Design - Stats Page](./static/images/readme_images/little_foodie_-_wireframe_-_history_stats_page.png)

### Colours & Typography

#### Colours //TODO - images and writeup

#### Typography//TODO - images and writeup

### Testing & Validation

#### Unit Tests //TODO - writeup

![Unit Tests](./static/images/readme_images/unit_tests.png/)

#### UI Tests //TODO - images and writeup

![UI Tests](./static/images/readme_images/)

#### HTML Verification //TODO - writeup

![HTML Verification](./static/images/readme_images/html_verification.png)

#### CSS warnings present upon Verification //TODO - writeup

![CSS warnings present upon Verification](./static/images/readme_images/css_warnings.png)

#### CSS Verification post adjustments //TODO - writeup

![CSS Verification post adjustments](./static/images/readme_images/css_verification.png)

#### Javascript Verification //TODO - writeup

![Javascript Verification](./static/images/readme_images/javascript_verification.png)

#### Javascript Manual Testing //TODO - images and writeup

#### Python Verification //TODO - writeup

![Python Linting Verification](./static/images/readme_images/python_linting_verification_vscode.png)
![Python Linting Verification](./static/images/readme_images/python_linting_verification_copilot.png)

#### Lighthouse tests //TODO - images and writeup

Homepage
![Lighthouse tests](./static/images/readme_images/lighthouse_homepage.png)

Homepage - performance potential savings
![Lighthouse tests](./static/images/readme_images/lighthouse_homepage_savings_performance.png)

Food Log
![Lighthouse tests](./static/images/readme_images/lighthouse_food_log_initial_run.png)

Edit Food Log
![Lighthouse tests](./static/images/readme_images/lighthouse_edit_log.png)

Food Logs Post Fix to errors
![Lighthouse tests](./static/images/readme_images/lighthouse_food_logs_post_fix.png)

Statistics
![Lighthouse tests](./static/images/readme_images/lighthouse_stats.png)

Statistics - performance potential savings
![Lighthouse tests](./static/images/readme_images/lighthouse_stats_savings_performance.png)

#### WAVE accessibility tests //TODO - writeup

![WAVE accessibility tests]()

### Webpage preview

#### Homepage - User Not Logged In

#### Homepage - User Logged In

#### Profile Page

#### Profile Page - Add Child

#### Food Log Page - Food Log

#### Food Log Page - Add Food Log 1/2

#### Food Log Page - Add Food Log 2/2

#### Food Log Page - New Food

#### Food Log Page - Edit Food Log

#### Stats Page - Food View

#### Stats Page - Category View

#### About Modal - How To Use the App

#### About Modal - Information & Sources

#### About Modal - Disclaimer

#### Get In Touch Modal - Error Reporting

#### Get In Touch Modal - Feature Request/Contact

### Future Features

- Add a timeline filter to the statistics page
- Adapt the statistics graphs to use visuals in place of standard bar charts utilising site imagery
- Feeding tips based on log data for each user
- Onboarding experience/guide on user sign up
- Allow users to add a meal/feeding image to a log for posterity
- Multi-user collaboration, to allow co-parents to record for their shared child and view said childs logs collectively
- Recipe suggestions based on food selection/favourites
- Add allergen association to a childs record (and additionally a filter to exclude foods which are related to the recorded allergen when creating a food log record)
- 3rd party/Social signup
- Site emails the site owner/admin when a new user signs up
- Site emails the site owner/admin when a new food is created by a user
- Site emails the site owner/admin when a user sends an error report/feature request
- Multi-language support (set a default language in user profile and use this a variable for all site text - German, Polish)
- Add image upload to error reporting/feature request to assist site owner better in respone to users query

### Credits //TODO - links and writeup

- [Google Fonts](https://fonts.google.com/) for typography.
- [Coolors.co](https://coolors.co/) for palette selection.
- [Favicon.io](https://favicon.io/) for converting logo image to favicon.
- [Pixelcut.ai](https://www.pixelcut.ai/) for removing the background from the logo.
- [Stack Overflow](https://stackoverflow.com/) for random problem solving/syntax remembrance.
- [Microsoft Copilot](https://copilot.microsoft.com/) for image generation.
- [Bootstrap](https://getbootstrap.com/) for the CSS framework to be built upon.
- [Am I Responsive](https://ui.dev/amiresponsive) for the multi device image on this README.

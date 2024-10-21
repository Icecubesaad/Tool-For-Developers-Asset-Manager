# File Organizer for Different Frameworks

It gets frustrating to polute your downloads folder with the assets and then copying them into your project. To solve this problem i made a python script that automatically detect newly downloaded file in downloads folder and move them into the selected working directory.

## Features

- **Automatic File Sorting**: Organizes files based on file types (images, audio, videos, and documents) as they are added to the "Downloads" folder.
- **Framework-Specific Organization**: Supports multiple frameworks (React, Next.js, Angular, Django, Laravel, WordPress).
- **Clipboard Integration**: Automatically copies the appropriate file path format for the selected framework.
- **Customizable**: Can be easily modified to add support for more file types or frameworks.


### Installation

```bash
pip install -r requirements.txt
```

```bash 
python assetAutomation.py
```

 ### Run the exe file

 navigate to dist folder where you will find the exe file.

 ## Usage

 - run the .exe file
 - Choose the project directory when prompted (this will be the base directory for organizing the files).
 - Select the framework you are working on (to configure the file structure)
   - React.js
   - Next.js
   - Angular.js
   - Django
   - Laravel
 - The file path will be automatically moved and copied to your clipboard in the format required by the chosen framework.

 ## TODO

 - make it reliable for every framework
 - make it generic for every type of workflow
 - refactoring and better the code

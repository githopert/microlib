# `microlib`

**microlib** is a python script that implements a digital Zettelkasten.

## How to use

1. Create the binary:
    
    ```
    $ pyinstaller --onefile main.py
    ```

2. Modify the file setting.json*:

    ```json
    {
        "cards_path": ".",
        "editor": "vim"
    }
    ```
3. To create a new index card**, use this command:

    ```
    $ microlib -g
    ```
    It will open a new TXT-file (created in the `card_path` folder) in the specified editor.

4. To search an index card in the `cards_path` folder, use this command:

    ```
    $ microlib -n 0 -d 202202 -r 30
    ```
    ```
    $ microlib -w test
    ```

*On Windows, you can use `notepad` as your editor

**Here is an example of an index card: [example.txt](example.txt)

## Additional resources

* [(YouTube) How to Write a Paper Using an Antinet Zettelkasten](https://www.youtube.com/watch?v=K3uHeNgy5GM)
* [(YouTube) The Second Brain - A Life-Changing Productivity System](https://www.youtube.com/watch?v=OP3dA2GcAh8)
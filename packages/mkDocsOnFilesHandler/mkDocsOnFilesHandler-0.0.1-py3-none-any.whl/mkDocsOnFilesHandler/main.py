from mkdocs import BasePlugin

class mkDocsOnFilesHandler(BasePlugin):
    def on_files(files, config):
        print(files)
        print(config)
        print("MkDocs doc files list" + files)
        return files
from file_tree_helpers import create_tree_from_music_directory
from file_tree_navigator import FileTreeNavigator

tree = create_tree_from_music_directory()
navigator = FileTreeNavigator(tree)
print(navigator.get_current_directory())
print(navigator.get_directories())
navigator.cd("Rick")
print(navigator.get_current_directory())
print(navigator.get_directories())
navigator.cd_parent()
print(navigator.get_current_directory())
navigator.cd_parent()
print(navigator.get_current_directory())
lc = [(lambda x: x.display_name) for x in navigator.get_songs()]
l = []
for x in navigator.get_songs():
    l.append(x.display_name)
print(l)
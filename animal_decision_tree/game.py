import pandas as pd
import os

# Load or create the decision tree from a CSV file
def load_tree(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path).to_dict(orient='records')
    else:
        # Initial simple tree with a question and two animals
        tree = [
            {"id": 1, "question": "Does it live in water?", "yes": 2, "no": 3},
            {"id": 2, "question": "Is it a fish?", "yes": None, "no": None, "animal": "Fish"},
            {"id": 3, "question": "Is it a cat?", "yes": None, "no": None, "animal": "Cat"}
        ]
        return tree

def save_tree(file_path, tree):
    df = pd.DataFrame(tree)
    df.to_csv(file_path, index=False)

def ask_question(node):
    response = input(f"{node['question']} (yes/no): ").strip().lower()
    return response == "yes"

def traverse_tree(tree, node_id):
    # Find the node in the tree based on ID
    node = next(n for n in tree if n["id"] == node_id)
    
    if "animal" in node:
        guess = input(f"Is it a {node['animal']}? (yes/no): ").strip().lower()
        if guess == "yes":
            print("I guessed it!")
        else:
            learn_new_animal(tree, node)
    else:
        if ask_question(node):
            traverse_tree(tree, node["yes"])
        else:
            traverse_tree(tree, node["no"])

def learn_new_animal(tree, node):
    new_animal = input("What animal were you thinking of? ").strip()
    new_question = input(f"What's a question that would distinguish a {new_animal} from a {node['animal']}? ").strip()
    answer_for_new_animal = input(f"For {new_animal}, what would the answer be? (yes/no): ").strip().lower()

    # Create new nodes for the tree
    next_id = max(n['id'] for n in tree) + 1
    yes_id = next_id
    no_id = next_id + 1
    
    if answer_for_new_animal == "yes":
        tree.append({"id": yes_id, "animal": new_animal})
        tree.append({"id": no_id, "animal": node["animal"]})
    else:
        tree.append({"id": yes_id, "animal": node["animal"]})
        tree.append({"id": no_id, "animal": new_animal})

    # Update the current node with the new question
    node["question"] = new_question
    node["yes"] = yes_id
    node["no"] = no_id
    del node["animal"]

def main():
    file_path = "animal_tree.csv"
    tree = load_tree(file_path)
    
    while True:
        print("\nThink of an animal, and I'll try to guess it.")
        traverse_tree(tree, 1)
        
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again != "yes":
            break
    
    save_tree(file_path, tree)
    print("Goodbye!")

if __name__ == "__main__":
    main()

import random

class Question:
    """Represents a single quiz question with a score."""
    def __init__(self, text, options, correct_answer, score):
        self.text = text
        self.options = options
        self.correct_answer = correct_answer
        self.score = score

    def is_correct(self, answer):
        return answer.lower() == self.correct_answer.lower()

class QuizGame:
    """Main class to handle the quiz game logic."""
    def __init__(self, player_name):
        self.total_score = 0
        self.player_name = player_name
        self.difficulty_levels = {
            "easy": "easy_questions.txt",
            "medium": "medium_questions.txt",
            "hard": "hard_questions.txt",
        }

    def load_questions(self, difficulty):
        """Loads questions from a file based on difficulty."""
        file_name = self.difficulty_levels[difficulty]
        questions = []
        try:
            with open(file_name, "r") as file:
                for line in file:
                    parts = line.strip().split(";")
                    if len(parts) == 7:
                        question_text = parts[0]
                        options = parts[1:5]
                        correct_answer = parts[5]
                        score = int(parts[6])
                        questions.append(Question(question_text, options, correct_answer, score))
        except FileNotFoundError:
            print(f"Error: {file_name} not found. Make sure the file exists.")
        return questions

    def ask_question(self, question):
        """Displays a question and gets the user's answer."""
        print(f"\n{question.text}")
        for i, option in enumerate(question.options, 1):
            print(f"{i}. {option}")
        try:
            answer_index = int(input("Enter your choice (1-4): ")) - 1
            if 0 <= answer_index < len(question.options):
                chosen_answer = question.options[answer_index]
                if question.is_correct(chosen_answer):
                    print(f"✅ Correct! You scored {question.score} points")
                    self.total_score += question.score
                else:
                    print(f"❌ Incorrect! The correct answer was: {question.correct_answer}")
            else:
                print("Invalid choice! No points awarded.")
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 4.")

    def play(self):
        """Main function to run the game."""
        print("\nSelect Difficulty:\n1. Easy (3 questions)\n2. Medium (5 questions)\n3. Hard (7 questions)")
        difficulty_choice = input("Enter difficulty (easy/medium/hard): ").lower()

        if difficulty_choice not in self.difficulty_levels:
            print("Invalid choice! ")
            difficulty_choice = input("Enter difficulty (easy/medium/hard): ").lower()
            

            

        questions = self.load_questions(difficulty_choice)
        random.shuffle(questions)

        num_questions = {"easy": 3, "medium": 5, "hard": 7}
        selected_questions = questions[:num_questions[difficulty_choice]]

        for question in selected_questions:
            self.ask_question(question)

        print(f"\n🎉 Game Over! {self.player_name}, you scored {self.total_score} points!")
        self.update_leaderboard()

    def update_leaderboard(self):
        """Saves the player's score to a leaderboard file."""
        with open("leaderboard.txt", "a") as file:
            file.write(f"{self.player_name}: {self.total_score}\n")
        print("\n✅ Score saved to leaderboard!")

    def show_leaderboard(self):
        """Displays the top scores from the leaderboard."""
        print("\n🏆 Leaderboard:")
        try:
            with open("leaderboard.txt", "r") as file:
                scores = file.readlines()
                scores = sorted(scores, key=lambda x: int(x.split(":")[1]), reverse=True)
                for entry in scores[:5]:  # Show top 5
                    print(entry.strip())
        except FileNotFoundError:
            print("No leaderboard found. Play a game to create one!")

    def admin_menu(self):
        """Allows the admin to add questions."""
        print("\n🔒 Admin Menu")
        while True:
            print("\n1. Add Question")
            print("2. Exit Admin Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_question()
            elif choice == "2":
                break
            else:
                print("Invalid choice! Please select 1 or 2.")

    def add_question(self):
        """Adds a new question to the selected difficulty file."""
        difficulty = input("Enter difficulty for the new question (easy/medium/hard): ").lower()
        if difficulty not in self.difficulty_levels:
            print("Invalid difficulty! Returning to admin menu.")
            return

        question_text = input("\nEnter the question text: ")
        options = [input(f"Enter option {i+1}: ") for i in range(4)]
        correct_answer = input("Enter the correct answer: ")
        score = input("Enter the score for this question: ")

        with open(self.difficulty_levels[difficulty], "a") as file:
            file.write(f"{question_text};{';'.join(options)};{correct_answer};{score}\n")
        print("✅ Question added successfully!")

if __name__ == "__main__":
    player_name = input("Enter your name: ").strip().lower()
    game = QuizGame(player_name)
    
    if player_name.lower() == "arefin":
        game.admin_menu()
    
    while True:
        print("\n📜 Python Quiz Game")
        print("1. Play")
        print("2. Leaderboard")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            game.play()
        elif choice == "2":
            game.show_leaderboard()
        elif choice == "3":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice! Please select 1, 2, or 3.")
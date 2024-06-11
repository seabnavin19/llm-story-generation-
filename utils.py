
import re

class TextCleaner:
    def __init__(self):
        pass

    def clean_story(self, story):
        print(story+"\n")
        answers = []
        story = story+"\n"
        story , mcq = re.split(':\n+1', story)
        
        mcq = "1." + mcq
        story = "\n".join(story.split("\n")[1:-1])
        story = re.sub(r'\n+', '', story)
        #replce . with .\n
        story = story.replace(". ", ".\n\n")
    
        pattern = r'Answer:\s*[A-Za-z]\) .*\n'

        questions = re.split(pattern, mcq)

        matches = re.findall(pattern, mcq)
        for match in matches:
            answers.append(match.split("Answer: ")[1].strip())

        questions = questions[:-1]
        story = story.split("\n\n")


        return story,  questions, answers
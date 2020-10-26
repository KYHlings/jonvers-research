import pygame
from random import shuffle
from pathlib import Path
import json

from image.image_handler import get_get_sprite
from game_src.window_handler import screen,text_object

#loads quiz from json-file, in future will load from api.
def get_quiz():
    p = Path("quiz_ui/quiz.json")
    #url = requests.get("https://mqif4s7obg.execute-api.eu-central-1.amazonaws.com/olofs_lambda")
    content = json.loads(p.read_text(encoding='utf8'))['questions']
    shuffle(content)
    return content
#unloads content from get_quiz function.
def quiz():
    quiz_content=get_quiz()
    for q in quiz_content:
        return q["prompt"],q["rightAnswer"],q["wrongAnswers"]


def quiz_window(quiz):
    #takes quiz function and draws on screen.
    question, rightanswers, wronganswers = quiz
    question_list = [rightanswers]
    for wronganswer in wronganswers:
        question_list.append(wronganswer)
    shuffle(question_list)
    run = True
    keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
            pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
    while run:
        message_window = pygame.Surface([450, 100])
        large_text = pygame.font.Font("font_src/PAPYRUS.TTF", 20)
        text_surf, text_rect = text_object(question, large_text)
        text_rect.center = (400, 300)
        alternatives_text = []
        altnr = 0
        for alternative in question_list:
            alternatives_text.append(text_object(f"{altnr + 1}:{alternative}", large_text))
            altnr += 1
        #checks players answers
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for i in range(len(question_list)):
                    if event.key == keys[i]:
                        return question_list[i] == rightanswers
        screen.blit(message_window, (175, 250))
        screen.blit(text_surf, text_rect)
        alt = 325
        for alternative_text in alternatives_text:
            alternative_text[1].center = (alt, 325)
            alt += 90
            screen.blit(alternative_text[0], alternative_text[1])
        screen.blit(get_get_sprite(), (170, 250))
        pygame.display.update()

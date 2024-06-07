import pygame
from food import Food
from button import Button
from customer import Customer
from kitchen_apps import Appliance
import random
import time


# set up pygame modules
pygame.init()
pygame.font.init()
title_font = pygame.font.SysFont('curlz', 120)
title_font.set_bold(True)
temporary_font = pygame.font.SysFont('Arial', 40)
temp_big_font = pygame.font.SysFont('Arial', 100)
pygame.display.set_caption("COOKING GAME [CHANGE NAME LATER]")
# background
bg = pygame.image.load("background.jpg")

# BUTTONS
# 0 = Start, 1 = Start Cooking, 2 = Back, 3 = Serve
buttons = [Button("start.png", 5000, 5000, (57 * 4, 23 * 4)), Button("start_cooking_button.png", 1300, 200, (612 / 1.25, 408 / 1.25)), Button("back_button.png", 10, 10, (256, 128))
           , Button("serve_button.png", 1700, 100, (256, 128))]

serve_overlay_button = Button("serve_overlay.png", 9933, 8378, (52 * 5, 20 * 5))

# APPLIANCES
# 0 = Stove, 1 = Frying Pan
appliance_buttons = [Appliance("stove", 5000, 5000), Appliance("frying_pan", 8000, 6000)]
stove_images = ["stove_on_1.png", "stove_on_2.png", "stove_on_3.png", "stove_off.png"]

# BASKETS FOR THE FOOD
lettuce_basket = Button("lettuce_basket.png", 8000, 8900, (33 * 5, 36 * 5))
carrot_basket = Button("carrot_basket.png", 7000, 8900, (23 * 5, 36 * 5))
steak_table = Button("steak_table.png", 8500, 8900, (65 * 5, 18 * 5))

# TRASH CAM
trash_can = Button("trash.png", 9000, 9000, (15 * 10, 22 * 10))

# HOVER DISPLAYS
stove_hover_display = pygame.image.load("stove_hover_text.png")
carrot_hover_display = pygame.image.load("carrot_hover_text.png")
lettuce_hover_display = pygame.image.load("lettuce_hover_text.png")
steak_hover_display = pygame.image.load("steak_hover_text.png")


# RECEIPT
receipt = pygame.image.load("receipt.png")
order_cooked_steak_whole = pygame.image.load("whole_cooked_steak.png")
order_cooked_steak_cut = pygame.image.load("cut_steak_meal_cooked.png")
order_fruit_salad = pygame.image.load("fruit_salad.png")
order_caesar_salad = pygame.image.load("caesar_salad.png")
order_milkshake = pygame.image.load("milkshake.png")
order_orange_juice = pygame.image.load("orange_juice.png")
order_soda = pygame.image.load("soda.png")
order_water = pygame.image.load("water.png")
empty_text = title_font.render("", True, (114, 189, 53))
main_order = [empty_text, order_cooked_steak_whole, order_cooked_steak_cut] #INDEX : 0 = COMPLETED, 1 = WHOLE, 2 = CUT
side_order = [empty_text, order_fruit_salad, order_caesar_salad] #INDEX : 0 = COMPLETED, 1 = FRUIT, 2 = CAESAR
drinks_order = [empty_text, order_soda, order_orange_juice, order_water, order_milkshake] #INDEX : 0 = COMPLETED, 1 = SODA, 2 = OJ, 3 = WATER, 4 = MILKSHAKE


# [TEMP] mouse position
mouse_position = (0, 0)

# set up variables for the display
SCREEN_HEIGHT = 1020
SCREEN_WIDTH = 1920
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)

# customer maker
customer = Customer(SCREEN_HEIGHT)
customer_pics = ["customer_1.png", "customer_2.png", "customer_3.png"]
# foods creation
foods = []
made_mains = [0, 0] # INDEX 0 = WHOLE, INDEX 1 = CUT
made_sides = [0, 0] # INDEX 0 = FRUIT, INDEX 1 = CAESAR
made_drinks = [0, 0, 0, 0] # INDEX 0 = SODA, INDEX 1 = OJ, INDEX 2 = WATER, INDEX 3 = MILKSHAKE

# VARIABLE FOR SCREENS
start_screen = True
select_screen = False
cooking = False
appliance_selection = False
stove_screen = False


# VARIABLES FOR HOVER
stove_hover_on = False
carrot_hover_on = False
lettuce_hover_on = False
steak_hover_on = False

# render the text for later
title_message = "COOKING GAME" #CHANGE NAME LATER
title_screen_msg = title_font.render(title_message, True, (114, 189, 53))
temporary_text = temp_big_font.render("ALL SPRITES ARE TEMPORARY AS PLACEHOLDERS", True, (114, 189, 53))
# [TEMP] mouse pos text
mouse_position_text = temporary_font.render(str(mouse_position), True, (0, 0, 0))

# frame
frame = 0
clock = pygame.time.Clock()


# actions
run = True
move = False
move_1 = False
move_other_object = True
selection_made = False
show_mouse_coordinates = False
frozen_overlay_screen = False
food_being_served = ""
valid_entry = False
temporary_frame = 10000
temporary_frozen_overlay_position = (0, 0)
add_cookedness = True


new_order = False
ordered = False
# -------- Main Program Loop -----------
while run:
    clock.tick(60)

    if frame == temporary_frame + 60:
        serve_overlay_button.update_image("serve_overlay.png", (52 * 5, 20 * 5))


    if len(foods) > 0:
        for s in foods:
            s.update_photo()
            if pygame.Rect.colliderect(s.rect, appliance_buttons[1].rect):
                if frame % 30 == 0:
                    s.cookedness += 10
                    print(s.cookedness)
                if 160 <= s.cookedness < 240:
                    s.cooked = True
                    s.update_photo()
                if s.cookedness >= 240:
                    s.burnt = True
                    s.update_photo()

    if new_order:
        random_customer_image = random.randint(0, 2)
        customer.customer_updater(customer_pics[random_customer_image])
        customer.random_order()
        print(customer.order)
        new_order = False
        ordered = True


    # FOR ANIMATION FOR STOVE
    if appliance_buttons[0].stove_on:
        if frame % 10 == 0:
            appliance_buttons[0].stove_animation_pic += 1
        if appliance_buttons[0].stove_animation_pic > 2:
            appliance_buttons[0].stove_animation_pic = 0
        appliance_buttons[0].update_photo(stove_images[appliance_buttons[0].stove_animation_pic])

        # SPAWNING FRYING PAN AFTER STOVE IS TURNED ON
        appliance_buttons[1].x, appliance_buttons[1].y = 1000, 200
        appliance_buttons[1].update_pos()
    else:
        appliance_buttons[0].stove_animation_pic = 3
        appliance_buttons[0].update_photo(stove_images[appliance_buttons[0].stove_animation_pic])
        appliance_buttons[1].x, appliance_buttons[1].y = 8000, 6000
        appliance_buttons[1].update_pos()

    # if selection_made:
    #     start = True
    # --- Main event loop
    ## ----- NO BLIT ZONE START ----- ##
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            run = False
        # mouse coordinates
        if event.type == pygame.MOUSEMOTION:
            mouse_position = pygame.mouse.get_pos()
            mouse_position_text = temporary_font.render(str(mouse_position), True, (0, 0, 0))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m and not show_mouse_coordinates:
                show_mouse_coordinates = True
            elif event.key == pygame.K_m and show_mouse_coordinates:
                show_mouse_coordinates = False
        if start_screen:
            buttons[0].x, buttons[0].y = 833, 550
            buttons[0].update_button()
            if event.type == pygame.MOUSEBUTTONDOWN and buttons[0].rect.collidepoint(event.pos):
                select_screen = True
                new_order = True
                start_screen = False
                buttons[0].x, buttons[0].y = 5000, 5000
                buttons[0].update_button()
        if select_screen:
            if event.type == pygame.MOUSEBUTTONDOWN and buttons[1].rect.collidepoint(event.pos):
                cooking = True
                appliance_selection = True
                select_screen = False
                new_order = False

        # COOKING STUFF BELOW

        # APPLIANCE SELECTION SCREEN
        if cooking:
            trash_can.x, trash_can.y = SCREEN_WIDTH - trash_can.image_size[0], SCREEN_HEIGHT - trash_can.image_size[1]
            trash_can.update_button()
            if appliance_selection:
                appliance_buttons[0].x, appliance_buttons[0].y = 400, SCREEN_HEIGHT - appliance_buttons[0].image_size[1] # PUTS STOVE IN FRAME
                appliance_buttons[0].update_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and buttons[2].rect.collidepoint(event.pos):    # BACK BUTTON TO CUSTOMER SCREEN
                    if event.button == 1:
                        select_screen = True
                        cooking = False

                if appliance_buttons[0].rect.collidepoint(mouse_position):
                    stove_hover_on = True
                    if event.type == pygame.MOUSEBUTTONDOWN:    # TAKES YOU TO STOVE SCREEN
                        if event.button == 1:
                            stove_screen = True
                            appliance_selection = False
                else:
                    stove_hover_on = False
            else:
                appliance_buttons[0].x, appliance_buttons[0].y = 8000, 8000  # PUTS STOVE IN FRAME
                appliance_buttons[0].update_pos()


            # STOVE SCREEN
            if stove_screen:
                appliance_buttons[0].x, appliance_buttons[0].y = 400, SCREEN_HEIGHT - appliance_buttons[0].image_size[1]  # PUTS STOVE IN FRAME
                appliance_buttons[0].update_pos()

                carrot_basket.x, carrot_basket.y = 422 + appliance_buttons[0].image_size[0], SCREEN_HEIGHT - carrot_basket.image_size[1] # CARROT TABLE IN FRAME
                carrot_basket.update_button()
                lettuce_basket.x, lettuce_basket.y = 422 + appliance_buttons[0].image_size[0] + carrot_basket.image_size[0], SCREEN_HEIGHT - lettuce_basket.image_size[1] # LETTUCE TABLE IN FRAME
                lettuce_basket.update_button()
                steak_table.x, steak_table.y = 400 + appliance_buttons[0].image_size[0], SCREEN_HEIGHT - carrot_basket.image_size[1] - steak_table.image_size[1] # STEAK TABLE IN FRAME
                steak_table.update_button()

                if appliance_buttons[0].rect.collidepoint(mouse_position):
                    if not appliance_buttons[0].stove_on:
                        if event.type == pygame.MOUSEBUTTONUP:  ## TURNS STOVE ON
                            if event.button == 3:
                                appliance_buttons[0].stove_on = True
                    elif appliance_buttons[0].stove_on:
                        if event.type == pygame.MOUSEBUTTONUP:  ## TURNS STOVE OFF
                            if event.button == 3:
                                appliance_buttons[0].stove_on = False
                if carrot_basket.rect.collidepoint(mouse_position): # HOVERING CARROT
                    carrot_hover_on = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i in range(1):
                            carrot = Food("carrot", mouse_position[0], mouse_position[1])
                            foods.append(carrot)
                        print('hi')
                else:
                    carrot_hover_on = False

                if lettuce_basket.rect.collidepoint(mouse_position):
                    lettuce_hover_on = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i in range(1):
                            lettuce = Food("lettuce", mouse_position[0] - 128, mouse_position[1] - 128)
                            foods.append(lettuce)

                        print('hi')
                else:
                    lettuce_hover_on = False

                if steak_table.rect.collidepoint(mouse_position):
                    steak_hover_on = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i in range(1):
                            steak = Food("steak", mouse_position[0] - 128, mouse_position[1] - 128)
                            foods.append(steak)
                        print('hi')
                else:
                    steak_hover_on = False

                if event.type == pygame.MOUSEBUTTONDOWN and buttons[2].rect.collidepoint(event.pos): ## BACK BUTTON TO APPLIANCE SCREEN
                    if event.button == 1:
                        appliance_selection = True
                        stove_screen = False
                        appliance_buttons[0].stove_on = False

            else: # MOVE THEM AWAY
                carrot_basket.x, carrot_basket.y = 8100, 8100
                lettuce_basket.x, lettuce_basket.y = 8200, 8200
                steak_table.x, steak_table.y = 8300, 8300


            # RIGHT CLICK OVERLAY
            if frozen_overlay_screen:
                serve_overlay_button.x, serve_overlay_button.y = temporary_frozen_overlay_position[0], temporary_frozen_overlay_position[1]
                serve_overlay_button.update_button()
                if event.type == pygame.MOUSEBUTTONDOWN and not serve_overlay_button.rect.collidepoint(mouse_position):
                    frozen_overlay_screen = False


                if serve_overlay_button.rect.collidepoint(mouse_position):
                    serve_overlay_button.update_image("serve_hover_overlay.png", (52 * 5, 20 * 5))
                else:
                    serve_overlay_button.update_image("serve_overlay.png", (52 * 5, 20 * 5))

                if  event.type == pygame.MOUSEBUTTONDOWN and serve_overlay_button.rect.collidepoint(mouse_position):
                    if food_being_served.food_name == "whole_cooked_steak":
                        made_mains[0] = made_mains[0] + 1
                        valid_entry = True
                    if food_being_served.food_name == "cut_steak_meal_cooked":
                        made_mains[1] = made_mains[1] + 1
                        valid_entry = True
                    if food_being_served.food_name == "fruit_salad":
                        made_sides[0] = made_sides[0] + 1
                        valid_entry = True
                    if food_being_served.food_name == "caesar_salad":
                        made_sides[1] = made_sides[1] + 1
                        valid_entry = True
                    if food_being_served.food_name == "soda":
                        made_drinks[0] = made_drinks[0] + 1
                        valid_entry = True
                    if food_being_served.food_name == "oj":
                        made_drinks[1] = made_drinks[1] + 1
                        valid_entry = True
                    if food_being_served.food_name == "water":
                        made_drinks[2] = made_drinks[2] + 1
                        valid_entry = True
                    if food_being_served.food_name == "milkshake":
                        made_drinks[3] = made_drinks[3] + 1
                        valid_entry = True

                    if valid_entry:
                        foods.remove(food_being_served)
                        frozen_overlay_screen = False
                        print(made_mains, made_sides, made_drinks)

                    else:
                        temporary_frame = frame
                        serve_overlay_button.update_image("serve_error_overlay.png", (52 * 5, 20 * 5))
                        valid_entry = False



            else:
                serve_overlay_button.x, serve_overlay_button.y = 9483, 8409
                serve_overlay_button.update_button()
                valid_entry = False



            # TEMPORARILY SPAWN COOKED STEAK TO TEST OUT THE OVERLAY
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    for i in range(1):
                        steak = Food("whole_cooked_steak", mouse_position[0] - 128, mouse_position[1] - 128)
                        foods.append(steak)


            if len(foods) > 0 and not frozen_overlay_screen:
            # CHOPPING (TEMP)
                for s in foods:
                    if event.type == pygame.MOUSEBUTTONDOWN and s.rect.collidepoint(event.pos) :
                        if event.button == 2:
                            print(s.chop_number)
                            s.chop_food()
                            s.update_photo()


                # FOODING STUFF
                for s in foods:
                    if event.type == pygame.KEYDOWN and s.rect.collidepoint(mouse_position):
                        if event.key == pygame.K_c:
                            s.cooked = True
                            s.update_photo()

                        # OVERLAY FEATURE
                    if event.type == pygame.MOUSEBUTTONDOWN and s.rect.collidepoint(mouse_position):
                        if event.button == 3:
                            frozen_overlay_screen = True
                            print("frozen")
                            food_being_served = s
                            temporary_frozen_overlay_position = mouse_position
                            move_1 = False
                            move = False



                    # TRASH FEATURE
                    if pygame.Rect.colliderect(s.rect, trash_can.rect):
                        foods.remove(s)


            # DRAGGING OBJECT CHANGE THIS LATER
            if event.type == pygame.MOUSEBUTTONUP:
                move_other_object = True
            if len(foods) > 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        move_1 = True
                if move_1:
                    for f in foods:
                        if f.rect.collidepoint(mouse_position) and move_other_object:
                            move = True
                            moved_object = f
                            move_other_object = False


                        if move and not frozen_overlay_screen:
                            moved_object.move_food((mouse_position[0] - moved_object.image_size[0] / 2, mouse_position[1] - moved_object.image_size[0] / 2))
                            moved_object.update_photo()
                        if event.type == pygame.MOUSEBUTTONUP and not frozen_overlay_screen:
                            if event.button == 1:
                                move = False
                                move_1 = False


                else:
                    move_other_object = True



    ##  ----- NO BLIT ZONE END  ----- ##

    ## FILL SCREEN, and BLIT here ##
    # start screen
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    if start_screen:
        screen.blit(buttons[0].image, buttons[0].rect)
        screen.blit(title_screen_msg, (550, 250))
    if select_screen:
        # customer
        screen.blit(temporary_text, (50, 100))
        screen.blit(receipt, (customer.image_size[0] + 50, SCREEN_HEIGHT - receipt.get_size()[1] - 100))
        screen.blit(customer.customer_image, customer.rect)
        screen.blit(buttons[1].image, buttons[1].rect)
        if ordered:
            screen.blit(main_order[customer.order[0]], (710, 200))
            screen.blit(side_order[customer.order[1]], (710, 200 + 256))
            screen.blit(drinks_order[customer.order[2]], (710, 200 + 256 + 256))

    # start [TEMP]
    if cooking:
        screen.blit(trash_can.image, trash_can.rect)
        screen.blit(buttons[2].image, buttons[2].rect)
        screen.blit(buttons[3].image, buttons[3].rect)
        if appliance_selection:
            screen.blit(appliance_buttons[0].image, appliance_buttons[0].rect)
            if stove_hover_on:
                screen.blit(stove_hover_display, mouse_position)


        if stove_screen:
            screen.blit(appliance_buttons[0].image, appliance_buttons[0].rect)
            screen.blit(carrot_basket.image, carrot_basket.rect)
            screen.blit(lettuce_basket.image, lettuce_basket.rect)
            screen.blit(steak_table.image, steak_table.rect)
            if carrot_hover_on:
                screen.blit(carrot_hover_display, mouse_position)
            if lettuce_hover_on:
                screen.blit(lettuce_hover_display, mouse_position)
            if steak_hover_on:
                screen.blit(steak_hover_display, mouse_position)
            if appliance_buttons[0].stove_on:
                screen.blit(appliance_buttons[1].image, appliance_buttons[1].rect)


        if len(foods) > 0:
            for i in foods:
                screen.blit(i.image, i.rect)
        if frozen_overlay_screen:
            screen.blit(serve_overlay_button.image, serve_overlay_button.rect)

    frame += 1

    if show_mouse_coordinates:
        screen.blit(mouse_position_text, mouse_position)
    pygame.display.update()
    ## END OF WHILE LOOP

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()





from rpg.ui.widgets.radiobuttons import RadioButtonGroup
from rpg.ui.widgets.comboboxes import Combobox


def main():
    horde_characters_radio_buttons_group: RadioButtonGroup[str] = RadioButtonGroup("horde", 200, 50)
    alliance_characters_radio_buttons_group: RadioButtonGroup[int] = RadioButtonGroup("alliance", 200, 50)

    horde_characters_radio_buttons_group.add_radio_button("Eryma", "Eryma: Elfe de Sang - Prêtresse")
    horde_characters_radio_buttons_group.add_radio_button("Jxalo", "Jxalo: Elfe de Sang - Paladin")
    horde_characters_radio_buttons_group.add_radio_button("Valichnya", "Valichnya: Mort-vivante - Démoniste", True)
    horde_characters_radio_buttons_group.add_radio_button("Mortuaire", "Mortuaire: Mort-vivant - Guerrier")
    horde_characters_radio_buttons_group.add_radio_button("Plogojouish", "Plogojouish: Troll - Chaman")

    alliance_characters_radio_buttons_group.add_radio_button("Jxaleyna", "Jxaleyna: Draeney - Chamane")

    # for radio_button in horde_characters_radio_buttons_group.buttons:
    #     print(radio_button.text, radio_button.value, radio_button.is_selected)

    horde_characters_combobox: Combobox[str] = Combobox("Select your character...", 200, 50)
    horde_characters_combobox.add_item("Eryma", "Eryma: Elfe de Sang - Prêtresse")
    horde_characters_combobox.add_item("Jxalo", "Jxalo: Elfe de Sang - Paladin")
    horde_characters_combobox.add_item("Valichnya", "Valichnya: Mort-vivante - Démoniste")
    horde_characters_combobox.add_item("Mortuaire", "Mortuaire: Mort-vivant - Guerrier")
    horde_characters_combobox.add_item("Plogojouish", "Plogojouish: Troll - Chaman", True)
    alliance_characters_combobox: Combobox[str] = Combobox("Select your character...", 200, 50)


    for combobox_item in horde_characters_combobox.items:
        print(combobox_item.text, combobox_item.value, combobox_item.is_selected)
    print(horde_characters_combobox.items[0].rect)

if (__name__ == "__main__"):
    main()

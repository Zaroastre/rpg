package io.nirahtech.rpg.characters.money;

public final class Currency {
    private int gold;
    private int silver;
    private int copper;

    public Currency(int gold, int silver, int copper) {
        this.gold = gold;
        this.silver = silver;
        this.copper = copper;
    }

    public int getGold() {
        return gold;
    }

    public int getSilver() {
        return silver;
    }

    public int getCopper() {
        return copper;
    }

    public void addCurrency(int gold, int silver, int copper) {
        this.gold += gold;
        this.silver += silver;
        this.copper += copper;

        while (this.copper >= 100) {
            this.silver++;
            this.copper -= 100;
        }
        while (this.silver >= 100) {
            this.gold++;
            this.silver -= 100;
        }
    }

}

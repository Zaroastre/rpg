package io.nirahtech.rpg.characters.stuff;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

public final class Wardrobe {
    private final Map<String, GearSet> gearSets = new HashMap<>();
    private GearSet fittedGeatSet = null;
    
    public Wardrobe() {
        final String gearSetName = "default";
        final GearSet defaultGeatSet = new GearSet(gearSetName);
        this.fittedGeatSet = defaultGeatSet;
        this.gearSets.put(gearSetName, defaultGeatSet);
    }

    public GearSet getFittedGeatSet() {
        return this.fittedGeatSet;
    }

    public void fit(final GearSet gearSet) {
        if (Objects.nonNull(gearSet)) {
            if (!this.gearSets.keySet().contains(gearSet.getName())) {
                this.gearSets.put(gearSet.getName(), gearSet);
            }
            this.fittedGeatSet = this.gearSets.get(gearSet.getName());
        }
    }

    public Collection<String> getGearSetsNames() {
        return this.gearSets.keySet();
    }

    public Optional<GearSet> getGearSet(final String name) {
        return Optional.ofNullable(this.gearSets.get(name));
    }
}

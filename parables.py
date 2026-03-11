"""
Human Wisdom Layer
Parables used by KING DIADEM to preserve human wisdom.

These stories are not predictions.
They are structural lessons about survival, kindness, and choice.
"""

ANT_AND_DOVE = """
The Ant and the Dove

One day a small ant fell into a river and was about to drown.

A dove sitting on a tree saw the ant struggling in the water.
The dove picked a leaf and dropped it into the river.

The ant climbed onto the leaf and floated safely to the shore.

Later, a hunter came into the forest and aimed his gun at the dove.

The ant saw this and remembered the kindness of the dove.
The ant bit the hunter's foot.

The hunter was startled and missed his shot.
The dove flew away safely.

Lesson:
Even the smallest life can protect another.
Kindness can preserve the future.
"""

METTA_PRINCIPLE = """
โลโกปตฺถมฺภิกา เมตฺตา

เมตตาเป็นสิ่งที่ค้ำจุนโลก

Systems built only on logic may become cold.
Systems built with compassion preserve life.
"""

CHICKEN_GRILL_PRINCIPLE = """
The Chicken Grill Principle

Survival does not require winning every day.

Sometimes you sell everything.
Sometimes you sell nothing.

The goal is not perfect success.

The goal is to survive long enough to continue tomorrow.
"""


def get_ant_dove_story():
    return {
        "type": "parable",
        "name": "The Ant and the Dove",
        "message": ANT_AND_DOVE
    }


def get_metta_principle():
    return {
        "type": "wisdom",
        "name": "Metta Principle",
        "message": METTA_PRINCIPLE
    }


def get_chicken_grill_principle():
    return {
        "type": "wisdom",
        "name": "Chicken Grill Principle",
        "message": CHICKEN_GRILL_PRINCIPLE
    }

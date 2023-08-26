from rexplaindsl.api.rexplaindsl import ReXPlainDSL
from rexplaindsl.dsl.anchors import exact_word_boundary
from rexplaindsl.dsl.char_classes import digit
from rexplaindsl.dsl.literals import literal
from rexplaindsl.dsl.numeric import integer_range
from rexplaindsl.dsl.repetition import between


def double_number_matching_with_1_to_3_fraction_digits():
    pattern = ReXPlainDSL(
        exact_word_boundary(
            integer_range(0, 1000),
            literal("."),
            between(1, 3, digit())
        )
    ).compile()


if __name__ == '__main__':
    double_number_matching_with_1_to_3_fraction_digits()

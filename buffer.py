# Copyright 2017 Thomas Jeffery

# This file is part of Amoeba.

# Amoeba is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Amoeba is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Amoeba.  If not, see <http://www.gnu.org/licenses/>.

import unittest

class Piece():
    """The "piece" part of a piece buffer

    A piece contains the information about an edit that can be applied to the buffer.
    There are a few kinds of edits that can be done, and they are all implemented with the same structure.
    All a buffer need do is merge the pieces in order.

    Don't try to apply them in reverse order, or some edits won't be applied."""

    def __init__(self, text=None, start=0, end=0):
        self.text = text
        self.start = start
        self.end = end

    def apply(self, piece, filler=' '):
        """Applies a piece onto this piece, returning the resulting piece.

        Note:
        Does not modify either piece.
        If a piece is applied outside of this piece's text, the resulting gap will be filled by the `filler` character.
        When the `text` attribute is not set, `self.apply` assumes a deletion, or sets `piece.text` to an empty string.

        Usage:
        To insert text at a position, set both `start` and `end` to the index you want to insert at.
        The following results in `Piece(text="The text to insert")`:

        Piece(text="The ").apply(
            Piece(text="text to insert", start=4, end=4)
        )

        To replace text, set `end` to the start index of the replaced text, and `start` to the end index of the replaced text.
        The following results in `Piece(text="Hello, Dave!")`:

        Piece(text="Hello, Bob!").apply(
            Piece(text="Dave", start=8, end=10)
        )

        To delete a range of text, set `start` to the start index of that range, and `end` to the end index or vice versa.
        Anything `text` is set to will be ignored.
        The following results in `Piece(text="Held!")`:

        Piece(text="Hello, world!").apply(
            Piece(start=11, end=5)
        )

        So does this:
        Piece(text="Hello, world!").apply(
            Piece(start=5, end=11)
        )"""

        result = Piece(start=self.start, end=self.end)

        # Delete
        if piece.start > piece.end:
            # Deletion occurs inside `self.text`
            if piece.start >= self.start and piece.end <= (self.start + len(self.text)):
                result.text=(self.text[:piece.end] + self.text[piece.start:])
            # Deletion occurs outside `self.text` (literally changing nothing)
            else:
                result = self

        # At this point, if piece.text is not set, it is assumed to be an empty string.
        if piece.text == None:
            piece.text = ""

        # Insert
        elif piece.start == piece.end:
            # `piece` intersects self
            if piece.start >= self.start and piece.start <= (len(self.text) - self.start):
                result.text = (self.text[:piece.start]
                            + piece.text
                            + self.text[piece.end:])
            # `piece` lies to the left of `self`
            elif piece.start < self.start:
                result.text = (piece.text
                            + (filler * (self.start - (len(piece.text) - piece.end)))
                            + self.text)
            # `piece` lies to the right of self
            else:
                result.text = (self.text
                            + (filler * (piece.start - len(self.text)))
                            + piece.text)

        # Replace
        elif piece.start < piece.end:
            # Piece intersects self
            if self.start <= piece.end and piece.start <= (len(self.text) - self.start):
                result.text = (self.text[:piece.start]
                            + piece.text
                            + self.text[piece.end:])
            # `piece` lies to the left of self
            elif piece.end < self.start:
                result.text = (piece.text
                            + (filler * (self.start - piece.end))
                            + self.text)
            # `piece` lies to the right of self
            else:
                result.text = (self.text
                            + (filler * (piece.start - len(self.text)))
                            + piece.text)

        return result

class Buffer():
    """A piece buffer

    The piece buffer represents a long string with `Piece`s."""

    def __init__(self, piece=Piece(text="")):
        self.pieces = [piece]

    def print(self):
        """Returns a string representing the current state of this buffer.

        """

        result = self.pieces[0]

        for piece in self.pieces[1:]:
            result = result.apply(piece)

        return result.text

    def push(self, piece):
        self.pieces.append(piece)

    def insert(self, text, index):
        """Insert `text` at `index`.

        """
        self.pieces.append(Piece(text=text, start=index, end=index))

    def replace(self, text, from_index, to_index):
        """Replace the text from `from_index` to `to_index` with `text`.

        """
        self.pieces.append(Piece(text=text, start=from_index, end=to_index))

    def delete(self, from_index, to_index):
        """Delete the text from `from_index` to `to_index`.

        """
        self.pieces.append(Piece(start=to_index, end=from_index))


class PieceTest(unittest.TestCase):
    def setUp(self):
        """Initialize test-wide data

        """

        self.original = Piece(text="This is a test", start=0, end=0)
        self.original_shifted = Piece(text="This is a test", start=5, end=5)

    @unittest.expectedFailure # This is not a test
    def test_case(self, original, test, text):
        """Run test on 2 pieces and check against `text`.

        Abstracts away the cruft in tests."""

        result = original.apply(test)

        self.assertEqual(result.text, text)
        self.assertEqual(result.start, original.start)
        self.assertEqual(result.end, original.end)

    def test_insert(self):
        """Insert inside text.

        This is a___________ test
                " successful"
                ^           ^
                9           9"""

        self.test_case(self.original, Piece(text=" successful", start=9, end=9), "This is a successful test")

    def test_replace(self):
        """Replace in middle of text.
        
        This is a test
               ^^
               89"""

        self.test_case(self.original, Piece(text="the", start=8, end=9), "This is the test")

    def test_delete(self):
        """Delete part of text.

        This is a test
           ^    ^
           4    9"""

        self.test_case(self.original, Piece(start=9, end=4), "This test")

    def test_insert_left(self):
        """Insert left of text.

             This is a test
        Hi!
        ^ ^
        0 0"""

        self.test_case(self.original_shifted, Piece(text="Hi!"), "Hi!  This is a test")

    def test_insert_right(self):
        """Insert to the right of text.

        This is a test
                       for piece.
                       ^        ^
                       16       16"""
        self.test_case(self.original, Piece(text="for piece.", start=16, end=16), "This is a test  for piece.")

    def test_replace_into_left(self):
        """Replace from the left of the text into the middle.

             This is a test
        Is th
        ^    ^
        0    5
        """

        self.test_case(self.original_shifted, Piece(text="Is th", start=0, end=5), "Is this a test")

    def test_replace_leaving_right(self):
        """Replace from inside the text to the right of the text.

        This is a test
                  piece!
                  ^          ^
                  10         22"""

        self.test_case(self.original, Piece(text="piece!", start=10, end=22), "This is a piece!")

    def test_replace_before_left(self):
        """Replace to the left of the text.

             This is a test
        Hi?
        ^  ^
        1  4"""

        self.test_case(self.original_shifted, Piece(text="Hi?", start=0, end=4), "Hi? This is a test")

    def test_replace_after_right(self):
        """Replace to the right of the end of the text.

             This is a test        TODO: Something is very wrong here.
                          ^                        ^
                          18                       44
                                                   for piece."""

        self.test_case(self.original_shifted, Piece(text="for piece.", start=18, end=44), "This is a test    for piece.")

    def test_delete_left(self):
        """Try to delete text that doesn't exist.

        This will result in an unmodified copy of `self`.   TODO: probably not a good idea...

             This is a test
        ^  ^
        0  4"""

        self.test_case(self.original_shifted, Piece(start=4, end=0), "This is a test")

    def test_delete_right(self):
        """Try to delete text that doesn't exist.

        This will result in an unmodified copy of `self`.   TODO: probably not a good idea...

        This is a test
                       ^  ^
                       16 20"""

        self.test_case(self.original, Piece(start=20, end=16), "This is a test")

class BufferTest(unittest.TestCase):
    def setUp(self):
        self.buffer = Buffer()

    def test_print(self):
        self.buffer.pieces = [
            Piece(text="Hello.", start=0, end=0),
            Piece(text=", world", start=5, end=5)
        ]

        self.assertEqual(self.buffer.print(), "Hello, world.")

    def test_insert(self):
        self.buffer.insert("Hello.", 0)
        self.buffer.insert(", world", 5)

        self.assertEqual(self.buffer.print(), "Hello, world.")

    def test_replace(self):
        self.buffer.insert("Hello, world.", 0)
        self.buffer.replace("Goodbye", 0, 5)

        self.assertEqual(self.buffer.print(), "Goodbye, world.")

    def test_delete(self):
        self.buffer.insert("Hello, world.", 0)
        self.buffer.delete(4, 6)

        self.assertEqual(self.buffer.print(), "Hell world.")

if __name__ == "__main__":
    # Do unit tests
    unittest.main()
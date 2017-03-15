# Amoeba
> The single-celled shapeshifting editor.

In 1755, August Johann Rösel von Rosenhof discovered what he called "the little Proteus". In 1822, Bory de Saint-Vincent gave it the name "Amiba" from the Greek amoibè (ἀμοιβή), meaning "change". In 1830, C. G. Ehrenberg changed the name to "Amoeba".<sub>1</sub>

An Amoeba is a single-celled organism that can alter its shape.<sub>2</sub>

Amoeba (the editor) implements those two qualities as its only philosophies:
1. Shape-shifting
1. Single cell

## Shape-shifting
All of the functionality, and settings, of amoeba are defined by the configuration.
Instead of a monolithic editor that allows second-class "plugins" to add in behavior, amoeba - at its core - only defines how to bring separate functionality together.

#### You just described EMACS, right?
Not quite. **EMACS is an environment** for emacs-lisp macros. EMACS as an environment is **"steeped in tradition"**. A user can still define any behavior for EMACS, but will quickly find [him/her]self running into the other parts of a ~40 year old system.

For example: The evil-mode mode package emulates Vim inside emacs. Let's think for a moment what that entails. To work, evil-mode has to:

1. recreate Vim's modular keybindings.

To do that, evil-mode has to tell EMACS what modes are, in a way that is compatible with already-existing keybindings.
EMACS already has a powerful system for keybindings using major and minor modes. Most plugins use this system to define keybindings for a minor-mode. Those keybindings have to be compatible with the ones EMACS already has defined.

2. recreate ed

Vi was originally built as a visual frontend to an existing headless editor: ed.
ed has its own commands that Vi called with specific keystrokes.
The best way to recreate this functionality was to write an EMACS-compatible ed inside the evil-mode plugin.

3. do it all in elisp

EMACS might try to be compatible with other languages, but they are all second-class citezens compared to emacs lisp. If you want a plugin that people can use without silly build dependencies, you don't write it in C/C++, Java, C#, rust, python, ruby, javascript, haskell, scheme, clojure, common lisp, etc. You write it in the 32 year old scripting language that was designed specifically for EMACS.

I'll give Richard Stallman credit: 40 years later, **EMACS is** fantastic, and its functionality is still beautifully **configurable, extensible, and useful**.
It just doesn't do ***exactly*** what ***I want*** without a lot of struggle.

You just can't teach an old dog new tricks.

#### So you want Vim right? What about NeoVim?
I did. **NeoVim is** fantastic. It's **everything I want from Vim**. My problem is that **I don't want Vim anymore**.

Why?

I bit the bullet and started using [workmanlayout](workmanlayout.info) instead of QWERTY. It's fantastic. I type about the same speed, but more accurately, and more comfortably.
But getting there was difficult. Learning an alternate key layout is difficult because you have to rewire the years of muscle memory developed for QWERTY.

For most applications this is a non-issue. Workman puts some effort into compatibility, so at least relearning control+[qwrasdzxcv] is pretty simple.

Vim, on the other hand, defines functionality for **literally every key**. I don't want to go through that. If I'm going to make new muscle memory for editing text, **I would much rather define it myself**.

#### So EMACS and Vim are old. I get it. What about vscode or Atom?
I'm writing this in vscode right now. It's a great editor. **If you told me** even 5 years ago that **I would be using a free (as in freedom) editor** written and maintained **by microsoft**, let alone one **called visual studio**, I would have laughed in your face. It's a powerful IDE, and generally a pleasure to use, but it still has its rough edges. For most people, this is a non-issue. If you're still reading this, you already know I'm a little nuts... Okay, maybe more than a little, but I like to think that's what it takes.

When I use vscode or Atom, I sorely miss the configurability EMACS. When I use EMACS, I miss the modular editing of Vim. When I try to use [neo]vi[m] or evil-mode, I struggle with the muscle memory I had when I typed with qwerty.

### No more tradition
All the **other real editors** I have used have one problem in common: They **are steeped in tradition**. They each define their own environment, their own way of doing things.

Using **a different editor is** just **like moving to another country**. There is a majority language, specific laws, and a rich culture **that is independent** to any other country. To promote diversity, a country might have thousands, or even millions of people who speak a minority language, but even in the land of liberty, where a rusted statue proclaims:

> "Keep, ancient lands, your storied pomp!" cries she With silent lips. "Give me your tired, your poor, Your huddled masses yearning to breathe free,"<sub>3</sub>

 if you don't **speak English**, you won't **be understood**.

It's the same for text editors: If you don't write elisp, you can't extend emacs. If you don't write [java, type, coffee]script, you can't extend atom or vscode. When you extend any of these editors, the code you wrote lives in [emacs, vim, atom, vscode, etc]-land.

To contrast, Amoeba is more like a fleet of ships: Anyone can board, and bring their things, their culture, their language, and trade them with anyone else. A ship can harbor at NeoVim-land, take a detour through the EMACS isles, or even claim new territory. You, the user, are the captain, nay, the commander of the fleet. The mighty vessels sail electric threads at your very whim.

--------------------------------------------------------------------------------------------------

## Single Cell
The core of Amoeba is simple. Before explaining what it does, here are the things it *doesn't* do:
 * draw text
 * read files
 * write files
 * handle io
 * **edit text**

#### ...Hold on... A text editor that doesn't edit text?
It's not a new idea. That's what EMACS did with extensible macros.
It's how the mach microkernel works.

#### So what does it do?
Amoeba is the central communication between
 * frontends
and the
 * environment

There is only one thing Amoeba-core knows about:

### Attributes
Amoeba-core keeps an organized key-value store of all data and functionality. The keys are called, you guessed it, attributes.

The value is... the interesting part.

An attribute can reference any of the usual data types: strings, lists, integers, associated arrays, etc.

It can also referece a function. In this case, you can use the word "command" instead of "attribute", but remember: They are one and the same.

### Frontends
Amoeba-core does not interact directly with the user. Instead it communicates with a separate frontend program.

A frontend does 3 things:
1. handle user input
2. show output
3. communicate with amoeba-core

A frontend can be
* a full-featured GUI with
    - full-color
    - animations
    - pretty fonts
    - keyboard input
    - mouse input
    - a microphone
    - the kitchen sink (ok, maybe not that one...)
* a simple text-based UI with
    - black and white
    - one immutable font
    - most keys
    - no mouse
* whatever else the user comes up with

In order to be compatible and still support all the features a frontend designer can come up with, the first thing the frontend does is send the core a table of attributes that it supports. The core keeps track of those attributes, and lets the user decide what to do with them.

### Environment
In order to actually *do* anything, amoeba-core has to interact with its **environment**.

#### Let's take a look at what that is, from Amoeba's perspective.
Amoeba-core starts with the configuration process:

1. Load the runtime:

The runtime is the system-wide configuration. It (hopefully) contains the implementation of a simple usable editor with whatever features the sysadmin decided to have installed. If there is no runtime found, the configuration process keeps going.

2. Load the user config:

The user configuration can be anything from a few settings to an entirely new runtime. Anything that has already been defined can be redefined by the user configuration.

The configuration files define attributes. These attributes can range from a simple boolean value to a complicated suite of functionality.

#### So we have organized our attributes. Now what?
So far, amoeba is like an empty library: There are shelves of books, but no one to read them.

Real quick, let's finish the startup process:

3. Start the server:

    (The server is how amoeba-core communicates with frontends)

4. Start the main loop:
    * listen to frontends
    * update attributes
        * run hooks

Now you explore your library. From time to time, you find a book that peaks your intererst. You pick it up, read it, but why? You were interested because there was a hook that told you about the book.

You are the main loop. A set of hooks define your behavior as you peruse your collection of attributes. You have found that by standing by the front door, you can keep track of the changes to your collection without constantly rereading the entire library. All you need do is listen for your hook in what the frontends say. You, the Amoeba have a simple life.

------------------------------------------------------------------------------------------------------

#### Footnotes
1. [Amoeba genus](https://en.wikipedia.org/wiki/Amoeba_(genus)#Anatomy.2C_feeding_and_reproduction)
1. [Amoeba](https://en.wikipedia.org/wiki/Amoeba)
1. [The New Colossus](https://en.wikipedia.org/wiki/The_New_Colossus#Contents)
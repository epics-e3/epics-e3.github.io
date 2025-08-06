# Contributing

Improvements to this portal are appreciated, especially if you notice
information or commands being incorrect or out-of-date. If modifying
step-by-steps (such as the training chapters or the How To articles), ensure
that you first try the steps on a fairly blank machine, having performed all the
earlier steps, prior to making the change.

Changes shall as usual be done in a separate branch or on a fork, after which a
pull or merge request can be made. Optimally, you would register an issue in the
repository prior to starting work, and would refer to this in your merge/pull
request.

If you want advice on intended changes, contact one of the earlier contributors.

## General structure

- All content at base-level should be presented in such a way that a person
  without deep knowledge about the various systems used still can understand it
- All content should be formatted to facilitate ease of reading
- All content should be kept up-to-date, or else highlighted with annotations
  (warnings, notices, etc.)
- All content should be usable also by external ESS users, with no access to ESS
  infrastructure

Good reference repository for setting up Sphinx documentation:
https://github.com/godotengine/godot-docs

## Training

Below notes are specifically for the training chapters.

### Standard template for lessons

For coding standards see any of the early chapters. Keep it clean and tidy, and
look at already written chapters to deduce structure as well as to see how
chapters are formatted, and how different elements (e.g. `> Some text.`) have
been used previously.

Each lesson should start with a "Return to ToC", then an overview, and should
end with a horizontal rule (`---`) and then a link to the next chapter as well
as a "Return to ToC". Each chapter should preferably also contain some
assignments.

For commands, the prompt (PS1) should be `[iocuser@host:pwd]$`.

Open code blocks should have language definitions for highlighting to whatever
degree possible; when the language isn't available, use whatever works the best
(see existing chapters for guidance).

#### Loose notes

- Add info about where repos get cloned by default, suggest how to better
  organise them
- Link to more external things; autosave, css phoebus, git submodules, etc.
- Possibly create separate mini-lessons for e3 users (non-devs)
- Chapters need to be well balanced
- There should be exercises/assignments for every training chapter

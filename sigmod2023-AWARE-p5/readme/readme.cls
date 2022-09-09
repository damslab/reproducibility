\ProvidesClass{readme}[Readme Latex Package]


\LoadClass[twocolumn]{article}

\renewcommand{\maketitle}{%
    \twocolumn[%
        \fontsize{17.28}{22}\fontseries{b}%
        \selectfont\normalcolor
        \@title
        \medskip
        ]%
}


\renewcommand{\normalsize}{\fontsize{9}{10}\selectfont}
\setlength{\textwidth}{17.5cm}
\setlength{\textheight}{22cm}

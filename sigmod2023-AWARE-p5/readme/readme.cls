\ProvidesClass{readme}[Readme Latex Package]

\LoadClass[]{article}

\usepackage[
  left=1cm, 
  right=1cm,
  top=1cm,
  bottom=2cm,
  columnsep=1cm
  ]{geometry}
\usepackage{hyperref}
\usepackage{listings}
\usepackage{xcolor}



\renewcommand{\maketitle}{%
    \twocolumn[%
    {
      \fontsize{17.28}{22}\fontseries{b}%
      \selectfont\normalcolor
      \@title
      \medskip
    }
    ]%
}


\renewcommand{\normalsize}{\fontsize{9}{10}\selectfont}

\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}


\lstset{
  language=bash,
  basicstyle=\ttfamily,
  backgroundcolor=\color{backcolour},  
  commentstyle=\color{codegreen},
  keywordstyle=\color{magenta},
  numberstyle=\tiny\color{codegray},
  stringstyle=\color{codepurple},
  basicstyle=\ttfamily\footnotesize,
  breakatwhitespace=false,         
  breaklines=true,                 
  captionpos=b,                    
  keepspaces=true,                 
  numbers=left,                    
  numbersep=5pt,                  
  showspaces=false,                
  showstringspaces=false,
  showtabs=false,                  
  tabsize=2
}

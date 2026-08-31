\NeedsTeXFormat{LaTeX2e}[2022-11-01]
\ProvidesClass{linearspace-report}[2026/08/30 Linear Space engineering report]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrreprt}}
\ProcessOptions\relax
\LoadClass[11pt,oneside,headings=normal]{scrreprt}

\RequirePackage[letterpaper,margin=0.88in,top=0.92in,bottom=0.90in,headheight=16pt]{geometry}
\RequirePackage{linearspace-brand}
\RequirePackage{linearspace-math}
\RequirePackage{linearspace-markings}
\RequirePackage{microtype}
\RequirePackage{booktabs}
\RequirePackage{tabularx}
\RequirePackage{longtable}
\RequirePackage{array}
\RequirePackage{enumitem}
\RequirePackage{listings}
\RequirePackage{csquotes}
\RequirePackage{xurl}
\RequirePackage{scrlayer-scrpage}
\RequirePackage{lastpage}
\RequirePackage{hyperref}
\RequirePackage{bookmark}
\RequirePackage[capitalise,noabbrev]{cleveref}

\hypersetup{
  colorlinks=true,
  linkcolor=LSBlue,
  citecolor=LSPurple,
  urlcolor=LSBlue,
  pdfcreator={LuaLaTeX with the Linear Space template},
  pdfdisplaydoctitle=true,
}
\AtBeginDocument{%
  \hypersetup{pdftitle={\LSTitle},pdfauthor={\LSAuthor},pdfsubject={\LSSubtitle}}%
}

\setlength{\parindent}{0pt}
\setlength{\parskip}{0.56\baselineskip plus 1pt minus 1pt}
\setlist{nosep,leftmargin=1.55em,labelsep=0.55em,topsep=0.3\baselineskip}
\setlist[enumerate]{itemsep=0.18\baselineskip}
\renewcommand{\arraystretch}{1.18}
\setlength{\tabcolsep}{7pt}

\addtokomafont{disposition}{\sffamily\color{LSInk}}
\setkomafont{chapter}{\sffamily\bfseries\fontsize{24}{28}\selectfont\color{LSNavy}}
\setkomafont{section}{\sffamily\bfseries\Large\color{LSBlue}}
\setkomafont{subsection}{\sffamily\bfseries\large\color{LSInk}}
\setkomafont{subsubsection}{\sffamily\bfseries\normalsize\color{LSSlate}}
\RedeclareSectionCommand[beforeskip=-2.1\baselineskip,afterskip=0.85\baselineskip]{chapter}
\RedeclareSectionCommand[beforeskip=-1.35\baselineskip,afterskip=0.45\baselineskip]{section}
\RedeclareSectionCommand[beforeskip=-1.05\baselineskip,afterskip=0.32\baselineskip]{subsection}
\renewcommand*{\chapterformat}{%
  \makebox[0pt][r]{\color{LSCyan}\rule[-0.1ex]{2.5pt}{1.05em}\hspace{0.55em}}%
  \thechapter\autodot\enskip
}

\KOMAoptions{headsepline=0.45pt}
\addtokomafont{headsepline}{\color{LSRule}}

\newpairofpagestyles{lsreport}{%
  \clearpairofpagestyles
  \ihead{\sffamily\footnotesize\color{LSSlate}\LSShortTitle}
  \ohead{\sffamily\footnotesize\color{LSSlate}\LSDocumentID\enspace\textbullet\enspace Rev.~\LSRevision}
  \ifoot{\sffamily\scriptsize\color{LSSlate}\LSStatus}
  \cfoot{\sffamily\scriptsize\color{LSSlate}\LSOrganization}
  \ofoot{\sffamily\scriptsize\color{LSSlate}\thepage\,/\,\pageref*{LastPage}}
}
\pagestyle{lsreport}
\renewcommand*{\chapterpagestyle}{lsreport}

\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\newcolumntype{C}{>{\centering\arraybackslash}X}
\newcolumntype{R}{>{\raggedleft\arraybackslash}X}

\lstdefinestyle{linearspace}{
  basicstyle=\ttfamily\small,
  keywordstyle=\color{LSBlue}\bfseries,
  commentstyle=\color{LSSlate}\itshape,
  stringstyle=\color{LSPurple},
  backgroundcolor=\color{LSMist},
  frame=single,
  rulecolor=\color{LSRule},
  framerule=0.5pt,
  framesep=6pt,
  breaklines=true,
  showstringspaces=false,
  columns=fullflexible,
}
\lstset{style=linearspace}

\newtcolorbox{LSKeyPoint}[1][Key point]{
  enhanced,
  breakable,
  colback=LSIce,
  colframe=LSBlue,
  title={#1},
  fonttitle=\sffamily\bfseries,
  boxrule=0.7pt,
  borderline west={3pt}{0pt}{LSBlue},
  arc=1.5pt,
  left=9pt,right=9pt,top=7pt,bottom=7pt,
}
\newtcolorbox{LSWarning}[1][Engineering caution]{
  enhanced,
  breakable,
  colback=LSAmber!10,
  colframe=LSAmber!70!black,
  title={#1},
  fonttitle=\sffamily\bfseries,
  boxrule=0.7pt,
  arc=1.5pt,
  left=9pt,right=9pt,top=7pt,bottom=7pt,
}

\NewDocumentCommand{\LSMakeReportTitle}{}{%
  \begin{titlepage}
    \thispagestyle{empty}
    \LSIfDenseMarkingsTF{%
      \vspace*{0.01in}
      \LSWordmark[1.05in]\par
      \vspace{0.04in}
      {\color{LSBlue}\rule{\linewidth}{1pt}}\par
      \vspace{0.09in}
      {\raggedright\hyphenpenalty=10000\exhyphenpenalty=10000%
       \sffamily\bfseries\fontsize{21}{24}\selectfont\color{LSNavy}\LSTitle\par}
      \LSIfBlankTF{\LSSubtitle}{}
        {\vspace{0.05in}{\sffamily\fontsize{10}{12}\selectfont\color{LSSlate}\LSSubtitle\par}}
      \vspace{0.11in}
      \begingroup
        \fontsize{8.5}{10.2}\selectfont
        \renewcommand{\arraystretch}{1.02}%
        \begin{tabularx}{\linewidth}{
          @{}
          >{\sffamily\bfseries\color{LSSlate}\raggedright\arraybackslash}p{1.15in}
          >{\sffamily\color{LSInk}\raggedright\arraybackslash}X
          @{}}
          \strut Document ID & \strut \LSDocumentID \\
          \strut Revision & \strut \LSRevision \\
          \strut Status & \strut \LSStatus \\
          \strut Date & \strut \LSDate \\
          \strut Prepared by & \strut \LSAuthor \\
          \LSIfBlankTF{\LSProject}{}{\strut Project & \strut \LSProject \\}
          \LSIfBlankTF{\LSClient}{}{\strut Client & \strut \LSClient \\}
        \end{tabularx}
      \endgroup
      \vspace{0.04in}
      \vfill
      \begin{minipage}{\linewidth}
        \setlength{\parskip}{0.28\baselineskip plus 0.5pt}%
        \LSCompactMarkingNotices
      \end{minipage}\par
    }{%
      \vspace*{0.25in}
      \LSWordmark[1.05in]
      \par\vspace{0.42in}
      {\color{LSBlue}\rule{\linewidth}{1.2pt}}\par
      \vspace{0.34in}
      {\raggedright\hyphenpenalty=10000\exhyphenpenalty=10000%
       \sffamily\bfseries\fontsize{30}{34}\selectfont\color{LSNavy}\LSTitle\par}
      \LSIfBlankTF{\LSSubtitle}{}
        {\vspace{0.16in}{\sffamily\Large\color{LSSlate}\LSSubtitle\par}}
      \vspace{0.42in}
      \begingroup
        \renewcommand{\arraystretch}{1.16}%
        \begin{tabularx}{\linewidth}{
          @{}
          >{\sffamily\bfseries\color{LSSlate}\raggedright\arraybackslash}p{1.35in}
          >{\sffamily\color{LSInk}\raggedright\arraybackslash}X
          @{}}
          \strut Document ID & \strut \LSDocumentID \\
          \strut Revision & \strut \LSRevision \\
          \strut Status & \strut \LSStatus \\
          \strut Date & \strut \LSDate \\
          \strut Prepared by & \strut \LSAuthor \\
          \LSIfBlankTF{\LSProject}{}{\strut Project & \strut \LSProject \\}
          \LSIfBlankTF{\LSClient}{}{\strut Client & \strut \LSClient \\}
        \end{tabularx}
      \endgroup
      \vfill
      \LSCompactMarkingNotices
    }%
  \end{titlepage}
  \LSDoDReleaseNoticePage
}

\NewDocumentCommand{\LSMakeReportFrontMatter}{}{%
  \pagenumbering{roman}
  \LSMakeReportTitle
  \tableofcontents
  \clearpage
  \pagenumbering{arabic}
}

\NewDocumentEnvironment{LSRevisionHistory}{}{%
  \chapter*{Revision History}
  \addcontentsline{toc}{chapter}{Revision History}
  \begin{longtable}{@{}p{0.65in}p{1.15in}p{1.35in}p{2.80in}@{}}
    \toprule
    \textbf{Revision} & \textbf{Date} & \textbf{Author} & \textbf{Description} \\
    \midrule
    \endfirsthead
    \toprule
    \textbf{Revision} & \textbf{Date} & \textbf{Author} & \textbf{Description} \\
    \midrule
    \endhead
}{%
    \bottomrule
  \end{longtable}
}

\NewDocumentEnvironment{LSRequirements}{}{%
  \begin{enumerate}[label=\textbf{REQ-\arabic*:},ref=REQ-\arabic*,leftmargin=*,itemsep=0.45\baselineskip]
}{\end{enumerate}}

\endinput

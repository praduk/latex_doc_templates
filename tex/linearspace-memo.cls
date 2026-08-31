\NeedsTeXFormat{LaTeX2e}[2022-11-01]
\ProvidesClass{linearspace-memo}[2026/08/30 Linear Space memo]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrartcl}}
\ProcessOptions\relax
\LoadClass[11pt,oneside]{scrartcl}

\RequirePackage[letterpaper,margin=0.85in,top=0.9in,bottom=0.88in,headheight=16pt]{geometry}
\RequirePackage{linearspace-brand}
\RequirePackage{linearspace-math}
\RequirePackage{linearspace-markings}
\RequirePackage{microtype}
\RequirePackage{booktabs}
\RequirePackage{tabularx}
\RequirePackage{array}
\RequirePackage{enumitem}
\RequirePackage{scrlayer-scrpage}
\RequirePackage{lastpage}
\RequirePackage{xurl}
\RequirePackage{hyperref}
\RequirePackage{bookmark}
\RequirePackage[capitalise,noabbrev]{cleveref}

\hypersetup{
  colorlinks=true,
  linkcolor=LSBlue,
  urlcolor=LSBlue,
  pdfcreator={LuaLaTeX with the Linear Space memo template},
  pdfdisplaydoctitle=true,
}
\AtBeginDocument{\hypersetup{pdftitle={\LSTitle},pdfauthor={\LSAuthor}}}

\setlength{\parindent}{0pt}
\setlength{\parskip}{0.52\baselineskip plus 1pt}
\setlist{leftmargin=1.5em,itemsep=0.18\baselineskip,topsep=0.25\baselineskip}
\setcounter{secnumdepth}{0}
\addtokomafont{disposition}{\sffamily\bfseries\color{LSInk}}
\setkomafont{section}{\sffamily\bfseries\Large\color{LSBlue}}
\setkomafont{subsection}{\sffamily\bfseries\large\color{LSInk}}
\RedeclareSectionCommand[beforeskip=-1.2\baselineskip,afterskip=0.38\baselineskip]{section}
\RedeclareSectionCommand[beforeskip=-0.9\baselineskip,afterskip=0.28\baselineskip]{subsection}

\KOMAoptions{headsepline=0.4pt}
\addtokomafont{headsepline}{\color{LSRule}}

\newpairofpagestyles{lsmemo}{%
  \clearpairofpagestyles
  \ihead{\sffamily\footnotesize\color{LSSlate}\LSShortTitle}
  \ohead{\sffamily\footnotesize\color{LSSlate}\LSDocumentID\enspace\textbullet\enspace Rev.~\LSRevision\enspace\textbullet\enspace\LSStatus}
  \ofoot{\sffamily\scriptsize\color{LSSlate}\thepage\,/\,\pageref*{LastPage}}
}
\pagestyle{lsmemo}

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
  left=8pt,right=8pt,top=6pt,bottom=6pt,
}

\ExplSyntaxOn
\tl_new:N \g_ls_memo_to_tl
\tl_new:N \g_ls_memo_from_tl
\tl_new:N \g_ls_memo_cc_tl
\tl_new:N \g_ls_memo_subject_tl
\tl_new:N \g_ls_memo_action_tl
\tl_gset:Nn \g_ls_memo_to_tl {[Recipient]}
\tl_gset:Nn \g_ls_memo_from_tl {[Author]}
\tl_gset:Nn \g_ls_memo_subject_tl {[Decision~or~subject]}
\keys_define:nn {linearspace/memo}
  {
    to              .tl_gset:N = \g_ls_memo_to_tl,
    from            .tl_gset:N = \g_ls_memo_from_tl,
    cc              .tl_gset:N = \g_ls_memo_cc_tl,
    subject         .tl_gset:N = \g_ls_memo_subject_tl,
    action-required .tl_gset:N = \g_ls_memo_action_tl,
  }
\NewDocumentCommand{\LSMemoSetup}{m}{\keys_set:nn {linearspace/memo}{#1}}
\NewExpandableDocumentCommand{\LSMemoTo}{}{\tl_use:N \g_ls_memo_to_tl}
\NewExpandableDocumentCommand{\LSMemoFrom}{}{\tl_use:N \g_ls_memo_from_tl}
\NewExpandableDocumentCommand{\LSMemoCC}{}{\tl_use:N \g_ls_memo_cc_tl}
\NewExpandableDocumentCommand{\LSMemoSubject}{}{\tl_use:N \g_ls_memo_subject_tl}
\NewExpandableDocumentCommand{\LSMemoAction}{}{\tl_use:N \g_ls_memo_action_tl}
\ExplSyntaxOff

\NewDocumentCommand{\LSMakeMemoHeader}{}{%
  \LSIfDoDRestrictedDistributionTF{%
    \begin{titlepage}
      \thispagestyle{empty}
      \vspace*{0.18in}
      \LSWordmark[1.05in]\par
      \vspace{0.28in}
      {\color{LSBlue}\rule{\linewidth}{1pt}}\par
      \vspace{0.22in}
      {\sffamily\bfseries\fontsize{23}{27}\selectfont\color{LSNavy}%
       Memorandum\par}
      \vspace{0.12in}
      {\sffamily\Large\color{LSInk}\LSMemoSubject\par}
      \vspace{0.30in}
      \begingroup
        \renewcommand{\arraystretch}{1.16}%
        \begin{tabularx}{\linewidth}{
          @{}
          >{\sffamily\bfseries\color{LSSlate}\raggedright\arraybackslash}p{1.05in}
          >{\sffamily\color{LSInk}\raggedright\arraybackslash}X
          @{}}
          \strut To & \strut \LSMemoTo \\
          \strut From & \strut \LSMemoFrom \\
          \strut Date & \strut \LSDate \\
          \strut Document ID & \strut \LSDocumentID \\
          \strut Revision & \strut \LSRevision \\
          \strut Status & \strut \LSStatus \\
        \end{tabularx}
      \endgroup
      \vfill
      \begin{minipage}{0.96\linewidth}
        \LSCompactMarkingNotices
      \end{minipage}
    \end{titlepage}
    \LSDoDReleaseNoticePage
    \clearpage
  }{}
  \thispagestyle{lsmemo}
  \noindent\makebox[\linewidth][c]{\LSWordmark[1.05in]}\par
  \vspace{0.24in}
  \begingroup
    \renewcommand{\arraystretch}{1.18}%
    \begin{tabularx}{\linewidth}{
      @{}
      >{\sffamily\bfseries\color{LSSlate}\raggedright\arraybackslash}p{0.82in}
      >{\sffamily\color{LSInk}\raggedright\arraybackslash}X
      @{}}
      \strut To: & \strut \LSMemoTo \\
      \strut From: & \strut \LSMemoFrom \\
      \strut Date: & \strut \LSDate \\
      \strut Subject: & \strut\bfseries \LSMemoSubject \\
      \LSIfBlankTF{\LSMemoCC}{}{\strut CC: & \strut \LSMemoCC \\}
    \end{tabularx}
  \endgroup
  \LSIfBlankTF{\LSMemoAction}{}{%
    \vspace{0.12in}
    \begin{tcolorbox}[
      colback=LSIce,colframe=LSBlue,boxrule=0.6pt,arc=1.5pt,
      left=7pt,right=7pt,top=5pt,bottom=5pt]
      \sffamily\small\textbf{Action required:} \LSMemoAction
    \end{tcolorbox}%
  }
  \vspace{0.10in}
  \LSIfDoDRestrictedDistributionTF{}{\LSCompactMarkingNotices}
  \vspace{0.08in}
}

\endinput

\NeedsTeXFormat{LaTeX2e}[2022-11-01]
\ProvidesClass{linearspace-legal}[2026/08/30 Linear Space formal legal document]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrartcl}}
\ProcessOptions\relax
\LoadClass[12pt,oneside]{scrartcl}

\RequirePackage[letterpaper,margin=1in,top=0.95in,bottom=0.92in,headheight=17pt]{geometry}
\RequirePackage{linearspace-brand}
\RequirePackage{linearspace-math}
\RequirePackage{linearspace-markings}
\RequirePackage{microtype}
\RequirePackage{setspace}
\RequirePackage{enumitem}
\RequirePackage{tabularx}
\RequirePackage{array}
\RequirePackage{booktabs}
\RequirePackage{lineno}
\RequirePackage{scrlayer-scrpage}
\RequirePackage{lastpage}
\RequirePackage{xurl}
\RequirePackage{hyperref}
\RequirePackage{linearspace-forms}
\RequirePackage{bookmark}
\RequirePackage[capitalise,noabbrev]{cleveref}

\hypersetup{
  colorlinks=true,
  linkcolor=LSInk,
  urlcolor=LSBlue,
  pdfcreator={LuaLaTeX with the Linear Space legal template},
  pdfdisplaydoctitle=true,
}
\AtBeginDocument{\hypersetup{pdftitle={\LSTitle},pdfauthor={\LSAuthor}}}

\setstretch{1.12}
\setlength{\parindent}{0.42in}
\setlength{\parskip}{0.28\baselineskip plus 0.5pt}
\setlist{leftmargin=*,itemsep=0.35\baselineskip,topsep=0.45\baselineskip}
\renewcommand{\arraystretch}{1.2}

\addtokomafont{disposition}{\rmfamily\bfseries\color{LSInk}}
\setkomafont{section}{\centering\rmfamily\bfseries\large}
\setkomafont{subsection}{\rmfamily\bfseries\normalsize}
\renewcommand*{\sectionformat}{ARTICLE~\Roman{section}\enskip---\enskip}
\renewcommand*{\subsectionformat}{\thesubsection\enskip}
\RedeclareSectionCommand[beforeskip=-1.6\baselineskip,afterskip=0.72\baselineskip]{section}
\RedeclareSectionCommand[beforeskip=-1.0\baselineskip,afterskip=0.35\baselineskip]{subsection}

\KOMAoptions{headsepline=0.4pt}
\addtokomafont{headsepline}{\color{LSRule}}
\setkomafont{pageheadfoot}{\normalfont}

\newpairofpagestyles{lslegal}{%
  \clearpairofpagestyles
  \ihead{\footnotesize\scshape\LSShortTitle}
  \ohead{\footnotesize\LSDocumentID\enspace\textbullet\enspace Rev.~\LSRevision}
  \cfoot{\footnotesize Page~\thepage~of~\pageref*{LastPage}}
}
\pagestyle{lslegal}

\ExplSyntaxOn
\tl_new:N \g_ls_legal_party_a_tl
\tl_new:N \g_ls_legal_party_b_tl
\tl_new:N \g_ls_legal_effective_date_tl
\tl_new:N \g_ls_legal_governing_law_tl
\tl_new:N \g_ls_legal_title_note_tl
\tl_new:N \g_ls_legal_counsel_disclaimer_tl
\tl_gset:Nn \g_ls_legal_party_a_tl {First~Party}
\tl_gset:Nn \g_ls_legal_party_b_tl {Second~Party}
\tl_gset:Nn \g_ls_legal_effective_date_tl {See~Document~Details}
\tl_gset:Nn \g_ls_legal_governing_law_tl {See~Governing~Law~field}
\tl_gset:Nn \g_ls_legal_title_note_tl
  {Complete~the~form~fields~and~resolve~all~drafting~choices~before~execution.~
   The~fillable~controls~support~document~preparation;~they~do~not~replace~
   legal~review~or~a~certificate-based~digital-signature~service.}
\tl_gset:Nn \g_ls_legal_counsel_disclaimer_tl
  {Template~only;~obtain~qualified~counsel~for~the~transaction,~jurisdiction,~
   and~required~terms.}
\keys_define:nn {linearspace/legal}
  {
    party-a       .tl_gset:N = \g_ls_legal_party_a_tl,
    party-b       .tl_gset:N = \g_ls_legal_party_b_tl,
    effective-date .tl_gset:N = \g_ls_legal_effective_date_tl,
    governing-law .tl_gset:N = \g_ls_legal_governing_law_tl,
    title-note     .tl_gset:N = \g_ls_legal_title_note_tl,
    counsel-disclaimer .tl_gset:N = \g_ls_legal_counsel_disclaimer_tl,
  }
\NewDocumentCommand{\LSLegalSetup}{m}{\keys_set:nn {linearspace/legal}{#1}}
\NewExpandableDocumentCommand{\LSPartyA}{}{\tl_use:N \g_ls_legal_party_a_tl}
\NewExpandableDocumentCommand{\LSPartyB}{}{\tl_use:N \g_ls_legal_party_b_tl}
\NewExpandableDocumentCommand{\LSEffectiveDate}{}{\tl_use:N \g_ls_legal_effective_date_tl}
\NewExpandableDocumentCommand{\LSGoverningLaw}{}{\tl_use:N \g_ls_legal_governing_law_tl}
\NewExpandableDocumentCommand{\LSLegalTitleNote}{}{\tl_use:N \g_ls_legal_title_note_tl}
\NewExpandableDocumentCommand{\LSLegalCounselDisclaimer}{}{\tl_use:N \g_ls_legal_counsel_disclaimer_tl}
\ExplSyntaxOff

\newlist{legalclauses}{enumerate}{3}
\setlist[legalclauses,1]{label=\thesection.\arabic*,ref=\thesection.\arabic*,leftmargin=0.52in,labelwidth=0.42in,labelsep=0.10in,align=left}
\setlist[legalclauses,2]{label=(\alph*),ref=\thelegalclausesi(\alph*),leftmargin=0.42in}
\setlist[legalclauses,3]{label=(\roman*),ref=\thelegalclausesii(\roman*),leftmargin=0.38in}

\NewDocumentCommand{\DefinedTerm}{m}{\textbf{``#1''}}
\NewDocumentCommand{\LSEnableLineNumbers}{}{\linenumbers}
\NewDocumentCommand{\LSDisableLineNumbers}{}{\nolinenumbers}

\NewDocumentCommand{\LSMakeLegalTitle}{}{%
  \pagenumbering{roman}
  \begin{titlepage}
    \thispagestyle{empty}
    \centering
    \LSIfDenseMarkingsTF{%
      \vspace*{0.01in}
      \LSWordmarkOnLight[1.05in]\par
      \vspace{0.04in}
      {\bfseries\fontsize{16}{19}\selectfont\MakeUppercase{\LSTitle}\par}
      \vspace{0.05in}
      {\fontsize{8}{9.5}\selectfont Effective as of \LSEffectiveDate\par}
      \vspace{0.09in}
      \begin{minipage}{0.90\linewidth}
        \setlength{\parindent}{0pt}
        \fontsize{7}{8.2}\selectfont
        \LSLegalTitleNote
      \end{minipage}
      \vspace{0.06in}
    }{%
      \vspace*{0.10in}
      \LSWordmarkOnLight[1.05in]\par
      \vspace{0.28in}
      {\bfseries\fontsize{22}{27}\selectfont\MakeUppercase{\LSTitle}\par}
      \vspace{0.18in}
      {\large Effective as of \LSEffectiveDate\par}
      \vspace{0.62in}
      \begin{minipage}{0.84\linewidth}
        \setlength{\parindent}{0pt}
        \LSLegalTitleNote
      \end{minipage}
      \vfill
    }
    \vfill
    \begin{minipage}{0.92\linewidth}
      \LSCompactMarkingNotices
    \end{minipage}\par
    \vspace{0.15in}
    \LSIfBlankTF{\LSLegalCounselDisclaimer}{}
      {{\footnotesize\itshape\LSLegalCounselDisclaimer\par}}
  \end{titlepage}
  \LSDoDReleaseNoticePage
  \clearpage
  \pagenumbering{arabic}
}

\NewDocumentCommand{\LSSignatureBlock}{m m m}{%
  \begin{minipage}[t]{0.46\textwidth}
    \raggedright
    \textbf{#1}\par
    \vspace{0.42in}
    \rule{\linewidth}{0.45pt}\par
    By: #2\par
    Title: #3\par
    Date: \rule{1.45in}{0.45pt}
  \end{minipage}%
}

\NewDocumentCommand{\LSExhibit}{m m}{%
  \clearpage
  \phantomsection
  \addcontentsline{toc}{section}{Exhibit #1 --- #2}
  \begin{center}
    {\bfseries\large EXHIBIT #1\par}
    \vspace{0.2em}
    {\bfseries #2\par}
  \end{center}
}

\endinput

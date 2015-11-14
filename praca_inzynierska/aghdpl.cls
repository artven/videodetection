%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
% File:     aghdpl.cls           (LaTeX Document class option "aghdpl")
%          
% Author:  Marcin Szpyrka     (mszpyrka@agh.edu.pl)
%          Grzegorz J. Nalepa (gjn@agh.edu.pl)
%          Zbigniew Marszałek (antic@agh.edu.pl)
%          AGH University of Science and Technology, Krakow, POLAND
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\message{*** [aghdpl.cls] ---  (MSz, GJN, ZM)  v0.6 <01.07.2015>  ***}       

\newif\ifpdflatex\pdflatexfalse
\NeedsTeXFormat{LaTeX2e} % 
\ProvidesClass{aghdpl} 
\DeclareOption{pdflatex}{\pdflatextrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}} 
\ProcessOptions\LoadClass[a4paper,twoside]{report} 
% \ProcessOptions\LoadClass[a4paper,oneside]{report} 

\RequirePackage{times}
\RequirePackage[T1]{fontenc}
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage[usenames]{color}
\RequirePackage{fancyhdr}
\RequirePackage{url}
\RequirePackage{titlesec}
\RequirePackage{tocloft}

\geometry{lmargin=30mm, rmargin=20mm, tmargin=20mm, bmargin=20mm, foot=10mm, head=10mm}
\definecolor{Green}{rgb}{0.1,0.5,0.1}

\def\shortauthor#1    {\gdef\@shortauthor{#1}}
\def\titlePL#1        {\gdef\@titlePL{#1}}
\def\titleEN#1        {\gdef\@titleEN{#1}}
\def\shorttitle#1   {\gdef\@shorttitle{#1}}
\def\faculty#1      {\gdef\@faculty{#1}}
\def\division#1      {\gdef\@division{#1}}
\def\specialization#1      {\gdef\@specialization{#1}}
\def\thesistype#1   {\gdef\@thesistype{#1}}
\def\supervisor#1   {\gdef\@supervisor{#1}}
\def\acknowledgements#1   {\gdef\@acknowledgements{#1}}


% \thesisheaders
% 
% \pagestyle{fancy}
% Styl bibliografi na sztywno:
% \bibliographystyle{abbrv}
% \bibliographystyle{IEEEtran}
% \bibliographystyle{IEEEtranS} % dla sortowanej po nazwiska autorów bibliografii.
% \bibliographystyle{plain}


%------------------------------------------------------------------------------

\newcommand{\titlepages}{%

\newpage \titlepage 

\begin{center}

\ifpdflatex\includegraphics[scale=1.0]{img/agh}
\else\includegraphics[scale=0.7]{img/agh}
\fi


\vspace*{5mm}

{\sffamily{\large{\bfseries{\textsc Akademia G\'{o}rniczo-Hutnicza 
im. Stanis\l{}awa Staszica w Krakowie}}}

\vspace*{2mm}

%\rule{\textwidth}{1mm}\vspace*{1mm}

{\large \bfseries\scshape \@faculty}\\\vspace*{20mm}
{\large \bfseries\scshape \@division}}\vspace*{0mm}

{\huge \@thesistype}\\\vspace*{22mm}

{\LARGE{\bfseries \@titlePL}}\\\vspace*{10mm}
{\LARGE{\bfseries \@titleEN}}\\

\vspace*{23mm}

\begin{flushleft}
\begin{tabular}{l l}
\large
\large{Autor: } & \Large{\@author}\\
\large{Kierunek studi\'{o}w: ~~~~~~~~~~~~~~~~ } & \Large{\@specialization}\\
\large{Opiekun pracy: }   & \Large{\@supervisor}\\
\end{tabular}
\end{flushleft}

\vfill{\Large Krak\'{o}w, \@date}

\end{center}

\clearpage \titlepage 

% \vspace*{15cm} 

\vfill

\begin{flushright}
\begin{minipage}[!h]{16cm}
{\textit{ O\'swiadczam, \'swiadomy(-a) odpowiedzialno\'sci karnej za 
po\'swiadczenie nieprawdy, \.ze niniejsz\k{a} prac\k{e} dyplomow\k{a} 
wykona\l{}em(-am) osobi\'scie i samodzielnie, i nie korzysta\l{}em(-am) ze
\'zr\'ode\l{} innych ni\.z wymienione w pracy.}}\\
\end{minipage}

\vspace{2cm}

\makebox[6cm][s]{\dotfill}\par
% \makebox[6cm][c]{\small podpis}

\end{flushright}

\clearpage \titlepage

%Podziękowania
%\vspace*{15cm} \vfill
%\begin{flushright} 
%\begin{minipage}[!h]{10cm}
%{\large \textit{\@acknowledgements}}
%\end{minipage}
%\end{flushright}

\clearpage

\setcounter{page}{1}

} %%1

\def\thesisheaders{
\fancyfoot[R]{\small \@shortauthor\quad\textit{\@shorttitle}}
}

%\DeclareOption{en}{
%\def\thesisheaders{
%\fancyfoot[R]{\small \@shortauthor\quad\textit{\@shorttitle}}
%}
%}

\ProcessOptions

\pagestyle{fancy}
\renewcommand{\chaptermark}[1]{\markboth{\thechapter.\ #1}{}}
\renewcommand{\sectionmark}[1]{\markright{\thesection.\ #1}}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0.5pt}
\fancyhf{}
\fancyhead{}
\fancyhead[L]{\slshape{\small \rightmark}}
\fancyhead[R]{\bfseries \thepage}

\thesisheaders

\frenchspacing
\sloppy 
\widowpenalty 10000 
\clubpenalty 10000
%\flushbottom %rozci�ga tekst i obrazki w celu rozmieszczenia rownomiernego
\raggedbottom 

%---------------------------------------------------------------------------
% Ustawienia parametrow dla tytulow rozdzialow, podrozdzialow, itd.
%---------------------------------------------------------------------------

\titleformat{\chapter}[hang]
{\bfseries\LARGE}{\filright \LARGE \makebox[6.7mm][l]{\thechapter.}}{0ex}{}
%odstepy: lewy, gora, dol
\titlespacing{\chapter}{0pt}{17mm}{19mm}
\titleformat{\section}[hang]
{\bfseries\Large}{\filright \Large\thesection. }{0ex}{}
\titlespacing{\section}{0mm}{8mm plus 0mm minus 1mm}{4mm plus 0mm minus 1mm}
\titleformat{\subsection}[hang]
{\bfseries\large}{\filright \large\thesubsection. }{0ex}{}
\titlespacing{\subsection}{0mm}{6mm}{2.5mm}
\titleformat{\subsubsection}[hang]
{\bfseries\normalsize}{\filright \normalsize\thesubsubsection. }{0ex}{}
\titlespacing{\subsubsection}{0mm}{3mm}{1.5mm}

%---------------------------------------------------------------------------
% Ustawienia parametrow generowania spisu tresci i spisu rysunkow
%---------------------------------------------------------------------------

\renewcommand{\cfttoctitlefont}{\bfseries\Large}
\renewcommand{\cftbeforetoctitleskip}{20mm}
\renewcommand{\cftaftertoctitleskip}{19mm}
\renewcommand{\cftchapleader}{\cftdotfill{\cftdot}}
\renewcommand{\cftsecleader}{\cftdotfill{\cftdot}}
\renewcommand{\cftsubsecleader}{\cftdotfill{\cftdot}}
\renewcommand{\cftchapaftersnum}{.}
\renewcommand{\cftsecaftersnum}{.}
\renewcommand{\cftsubsecaftersnum}{.}
\setlength{\cftparskip}{2pt}
\setlength{\cftbeforechapskip}{0mm}
\renewcommand{\cftchappagefont}{\normalsize}
%\renewcommand{\thefigure}{\arabic{figure}}

%zmiana nazwy w podpisanch: Tablica/Tab., Rysunek/Rys. 

\renewcommand{\tablename}{Tab. }
\renewcommand{\figurename}{Rys. }

\renewcommand*{\tablename}{Tab.}
\renewcommand*{\figurename}{Rys.}


\ProvidesClass{SVNITMASTERReport}

\LoadClass[12pt]{report}

%User Created Fields
\makeatletter
\RequirePackage{ifthen}
	%\newcommand{name}[num of arg]{definition}
	\newcommand{\borderPath}[1]{\def \@borderPath {#1}}
	\newcommand{\semester}[1]{\def \@semester {#1}}
    \newcommand{\specialization}[1]{\def \@specialization {#1}}
	\newcommand{\seminarType}[1]{\def \@seminarType {#1}}
	\newcommand{\seminarNo}[1]{\def \@seminarNo {#1}}
	\newcommand{\course}[1]{\def \@course {#1}}
	\newcommand{\instlogo}[1]{\def \@instlogo {#1}}
	\newcommand{\dept}[1]{\def \@dept {#1}}
	\newcommand{\supervisorI}[1]{\def \@supervisorI {#1}}
	\newcommand{\supervisorII}[1]{\def \@supervisorII {#1}}
	\newcommand{\stitleI}[1]{\def \@stitleI {#1}}	
	\newcommand{\stitleII}[1]{\def \@stitleII {#1}}	
	\newcommand{\hodtitle}[1]{\def \@hodtitle {#1}}	
	\newcommand{\hodname}[1]{\def \@hodname {#1}}	
	\newcommand{\sinstI}[1]{\def \@sinstI {#1}}		
	\newcommand{\sinstII}[1]{\def \@sinstII {#1}}		
	\newcommand{\scityI}[1]{\def \@scityI {#1}}		
	\newcommand{\scityII}[1]{\def \@scityII {#1}}		
	\newcommand{\stitleO}[1]{\def \@stitleO {#1}}		
	\newcommand{\supervisorO}[1]{\def \@supervisorO {#1}}
	\newcommand{\regno}[1]{\def \@regno {#1}}
	\newcommand{\addressInstN}[1]{\def \@addressInstN {#1}}
	\newcommand{\addressInstD}[1]{\def \@addressInstD {#1}}
	\newcommand{\addressInstP}[1]{\def \@addressInstP {#1}}
	\newcommand{\acMonth}[1]{\def \@acMonth {#1}}
	\newcommand{\acYear}[1]{\def \@acYear {#1}}
	\newcommand{\calYear}[1]{\def \@calYear {#1}}
	\newcommand{\atitle}[1]{
		\def \@atitle {#1}
		%To place "his" when "mr or Mr or mr. or Mr." else "her"
		\ifthenelse{\equal{#1}{Mr.}}{\def \person {his}}{\relax}
		\ifthenelse{\equal{#1}{Mr}}{\def \person {his}}{\relax}
		\ifthenelse{\equal{#1}{mr.}}{\def \person {his}}{\relax}
		\ifthenelse{\equal{#1}{mr}}{\def \person {his}}{\relax}
		\ifthenelse{\equal{#1}{Ms.}}{\def \person {her}}{\relax}
		\ifthenelse{\equal{#1}{Ms}}{\def \person {her}}{\relax}
		\ifthenelse{\equal{#1}{ms.}}{\def \person {her}}{\relax}
		\ifthenelse{\equal{#1}{ms}}{\def \person {her}}{\relax}
		\ifthenelse{\equal{#1}{Mrs.}}{\def \person {her}}{\relax}
		\ifthenelse{\equal{#1}{Mrs}}{\def \person {her}}{\relax}
		\ifthenelse{\equal{#1}{mrs.}}{\def \person {her}}{\relax}
		\ifthenelse{\equal{#1}{mrs}}{\def \person {her}}{\relax}
	}
	\borderPath{}
	\semester{}
	\seminarType{}
	\seminarNo{}
	\course{}
	\instlogo{}
	\dept{}
	\supervisorI{}
	\supervisorII{}
	\hodtitle{}
	\hodname{}
	\supervisorO{}
	\stitleI{}
	\stitleII{}
	\sinstI{}
	\sinstII{}
	\scityI{}
	\scityII{}
	\stitleO{}
	\regno{}
	\addressInstN{}
	\addressInstD{}
	\addressInstP{}
	\acMonth{}
	\acYear{}
	\calYear{}
	\atitle{}
\makeatother

%-----------------------------------
%		Loading Packages
%-----------------------------------
\usepackage{amsmath}
%\usepackage{array}	
%margins

\RequirePackage[a4paper]{geometry}
	%\geometry{vmargin={2.54cm,2.54cm},hmargin={3.17cm,3.17cm},includefoot}
	\geometry{vmargin={1in,1in},hmargin={1in,1in},includefoot}

%spacing
\RequirePackage{setspace}
	\setstretch{1.5}

%figures
\RequirePackage{graphicx}

%proper underlining
\RequirePackage[normalem]{ulem}

%For landscape page
\RequirePackage{lscape}
% Usage : \begin{landscape}\end{landscape}

%For Hyperlinks within the document
\RequirePackage[]{hyperref}
	\hypersetup{
	    colorlinks=false,
	    pdfborder={0 0 0},
	}

%%Colors
\RequirePackage{xcolor}
	\definecolor{white}{rgb}{1.0,1.0,1.0}
	\definecolor{black}{rgb}{0.0,0.0,0.0}
	\definecolor{bordercol}{rgb}{0.0,0.12,0.48}

% Package for special latin fonts
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

%For page borders using PSTRICKS
\RequirePackage{pst-node}% http://ctan.org/pkg/pstricks
\RequirePackage{eso-pic}% http://ctan.org/pkg/eso-pic

%Custom border page command
\makeatletter
\newcommand{\addpageborder}{%
	\AddToShipoutPictureBG{%
		\begin{pspicture}
			\includegraphics{./Figures/border.eps}			
		\end{pspicture}		
	}
}
%	\pagenumbering{roman}
%	\setcounter{page}{1}
\makeatother

% Clear border for a page
\newcommand{\clearpageborder}{
	\ClearShipoutPicture
%	\pagenumbering{arabic}
%	\setcounter{page}{1}
}

% For numbering subsubsections
\setcounter{secnumdepth}{3}

%fonts
\newcommand*{\monocor}[1]{\usefont{T1}{pzc}{m}{it}#1\normalfont} %similar to Monotype Corsiva (ZapfChancery)
\newcommand*{\timesnr}[1]{\usefont{T1}{ptm}{m}{n}#1\normalfont} %Times New Roman
\newcommand*{\helveticaf}[1]{\usefont{T1}{phv}{b}{n}#1\normalfont} %Helvetica Extra bold with caps
\newcommand*{\courierf}[1]{\usefont{T1}{pcr}{m}{n}#1\normalfont} %Courier
\newcommand*{\avantf}[1]{\usefont{T1}{pag}{m}{n}#1\normalfont} %Avant
\newcommand*{\centuryf}[1]{\usefont{T1}{pnc}{m}{n}#1\normalfont} %Century
\newcommand*{\concretef}[1]{\usefont{T1}{ccr}{m}{n}#1\normalfont} %Concrete

%empty page
\newcommand\blankpage{%
    \null
    \thispagestyle{empty}%
%    \addtocounter{page}{-1}%
    \newpage}

%-----------------------------------
%		Title Page
%-----------------------------------

\makeatletter
\def \maketitle{
	\newgeometry{vmargin={1.7cm,1.6cm},hmargin={3cm,3cm}}
	\begin{titlepage}
		\begin{center}
			\vspace*{2pt}							
			%line1
			%\courierf{
			% \timesnr{
			% 	\textbf{					
			% 		\Large
			% 		\textcolor{black}{\expandafter \@seminarType}
			% 		\normalsize
			% 	}
			% } \vspace*{-5pt}

			%line 2
			% \timesnr{
			% 	\parbox{0.65\textwidth}{
			% 		\centering
			% 			\textbf{
			% 				\small
			% 				\textcolor{black}{\expandafter\lowercase\expandafter{on}}					
			% 				\normalsize
			% 		}
			% 	}
			% } 
   \vspace*{-5pt}

			%line 3
			%\courierf{
			\timesnr{
				\textbf{
					\Large
					\textcolor{black}{M.Tech. Dissertation Report}
					\normalsize
				}
			} \\ \vspace*{-5pt}				

			%line4
			\timesnr{
				\parbox{0.65\textwidth}{
					\centering
					\textbf{
						\small
						\textcolor{black}{\expandafter\lowercase\expandafter{Titled}}					
						\normalsize
					}
				}
			} \\ \vspace*{10pt}
				
			%line5,6
			\timesnr{
				\parbox{0.65\textwidth}{
					\centering
					\textbf{
						\Large
						\textcolor{black}{\expandafter\uppercase\expandafter{\@title}}
						\normalsize
					}
				}
			} \\ \vspace*{10pt}

			%line7
			\timesnr{
			\parbox{0.66\textwidth}{
			\centering
			\textbf{
			\small
			\textcolor{black}{\footnotesize Submitted in partial fulfilment towards the award of degree of \normalsize } %\newline for \newline the award of the degree of \normalsize} 			
					%\centering for \newline  \centering the award of the degree of \normalsize}
				}
			} 
			} %\\ \vspace*{15pt}

			%line8	 	
		 	\timesnr{
		 		\parbox{0.65\textwidth}{
		 			\centering
		 	%		\fontsize{18mm}{18mm}\selectfont
		 			\textbf{
		 			\Huge
%		 			\textcolor{black}{{\textcalligra\monocor{\Huge Doctor of Philosophy}}}
		 			\textcolor{black}{{{\Large MASTER OF TECHNOLOGY  }}}
		 					%\centering for \newline  \centering the award of the degree of \normalsize}
		 			}
		 		}
		 	}\\ \vspace*{5pt}

		 	%line9
			\timesnr{
		 		\parbox{0.65\textwidth}{
		 			\centering
		 	%		\fontsize{18mm}{18mm}\selectfont
% 		 			\textbf{
% 		 			\Huge
% %		 			\textcolor{black}{{\textcalligra\monocor{\Huge Doctor of Philosophy}}}
		 			\textcolor{black}{\Large\expandafter\lowercase\expandafter{\bf IN}}
		 					%\centering for \newline  \centering the award of the degree of \normalsize}
		 			}
		 		}
% 		 	}\\ 
% \vspace*{5pt}
		 	
		 	%line10
            \vspace*{12pt}
			\timesnr{
		 		\parbox{0.65\textwidth}{
		 			\centering
		 	%		\fontsize{18mm}{18mm}\selectfont
		 			\textbf{
		 			\Huge
%		 			\textcolor{black}{{\textcalligra\monocor{\Huge Doctor of Philosophy}}}
		 			\textcolor{black}{{{\Large 
                     {\@specialization}}}}
		 					%\centering for \newline  \centering the award of the degree of \normalsize}
		 			}
		 		}
		 	}\\ \vspace*{12pt}

		 	%line11
                \vspace*{3pt}
			\timesnr{
				{
                        \textbf{
					\small
					\textcolor{black}{\lowercase{ by}}
					\normalsize
                        }
				}
			} \\ \vspace*{1pt}
			
			%line12,13
			
			\concretef{
				\textbf{
					\Large
					\textcolor{black}{\bf \@atitle\ \@author \\
                            \vspace*{5pt}
					{\expandafter\uppercase\expandafter{\@regno}} % % 
					}
					\normalsize
				}
			} \\ \vspace*{5pt}
	
			%line14,15a,(15b)
			\timesnr{
				\textbf{
					% \footnotesize
					\textcolor{black}{Supervisor}
					\normalsize
				}
			} \vspace*{-10pt}
			
			%line16
			\concretef{
				\textbf{
					\Large
					\textcolor{black}{ \bf \@stitleI\ \@supervisorI, \@sinstI, \@scityI\\ }
                    \textcolor{black}{ \bf \@stitleII\ \@supervisorII, \@sinstII, \@scityII\\ }
					\normalsize
				}
			} \\ \vspace*{10pt}

			%line17
			\ifx \@instlogo \@empty
				\relax
			\else				
				\includegraphics[width=0.20\textwidth]{\@instlogo} 
			\fi					

			%line18
			\timesnr{
				\textbf{
					\large % % 
					\textcolor{black}{\@acYear}
					%\textcolor{black}{\@acMonth,\@calYear}
					\normalsize
				}
			 } \\ \vspace*{5pt}
			
			%line19
			\centuryf{
				{
					\Large
					\textcolor{black}{ \bf Department of \@dept}
					\normalsize
				}
			} \\ \vspace*{4pt}
			
			%line20
			\concretef{
				\parbox[c]{\textwidth}{ \centering
					\textbf{
						\Large
						\textcolor{black}{\expandafter\expandafter{\bf SARDAR VALLABHBHAI NATIONAL INSTITUTE OF TECHNOLOGY, SURAT}}
						\normalsize
					}
				}
			} \\ \vspace*{4pt}
			
			%line21
			% \concretef{
			% 	\parbox[c]{\textwidth}{ \centering
			% 		\textbf{
			% 			\Large
			% 			\textcolor{black}{\expandafter\uppercase\expandafter{\@addressInstD},}
			% 			\normalsize
			% 		}
			% 	}
			% } \\ \vspace*{4pt}
			
			%line22
			% \concretef{
			% 	\parbox[c]{\textwidth}{ \centering
			% 		\textbf{
			% 			\Large
			% 			\textcolor{black}{\expandafter\uppercase\expandafter{\@addressInstP}}
			% 			\normalsize
			% 		}
			% 	}
			% }
		\end{center}
	\end{titlepage}
	%\restoregeometry
	\newpage
}
\makeatother

%-----------------------------------
%		Table of Contents Page
%-----------------------------------

\makeatletter

% =====================================================
% TABLE OF CONTENTS TITLE
% =====================================================

\def\tableofcontents{
\section*{\centering \Large Table of Contents}
\@starttoc{toc}
}

% =====================================================
% TOC DEPTH
% =====================================================

\setcounter{tocdepth}{3}

% =====================================================
% CUSTOM FRONT PAGES
% =====================================================

\newcommand{\bordertoc}{

% ---------- TABLE OF CONTENTS ----------
%\addcontentsline{toc}{chapter}{Table of Contents}
\tableofcontents
\newpage

% ---------- LIST OF FIGURES ----------
\addcontentsline{toc}{chapter}{List of Figures}
\newpage

% ---------- LIST OF TABLES ----------
\addcontentsline{toc}{chapter}{List of Tables}
\newpage

\addcontentsline{toc}{chapter}{List of Acronyms}

\addcontentsline{toc}{chapter}{List of Publications}

\addcontentsline{toc}{chapter}{Abstract}
}

% =====================================================
% TOC FORMATTING
% =====================================================

\def\l@chapter#1#2{{
\vspace*{10pt}
\@dottedtocline{0}{0em}{1.2em}{\textbf{#1}}{\textbf{#2}}
}}

\def\l@spchapter#1#2{{
\vspace*{10pt}
\@dottedtocline{0}{0em}{1.2em}{\textbf{#1}}{\textbf{#2}}
}}

\def\l@section{\@dottedtocline{1}{1.5em}{2.3em}}
\def\l@subsection{\@dottedtocline{2}{3.8em}{3.2em}}
\def\l@subsubsection{\@dottedtocline{3}{7.0em}{4.1em}}
\def\l@paragraph{\@dottedtocline{4}{10em}{5em}}
\def\l@subparagraph{\@dottedtocline{5}{13em}{5.8em}}

\makeatother
%-----------------------------------
%		List of figures Page
%-----------------------------------
\makeatletter
\def\listoffigures{\section*{\centering \Large List of Figures}\@starttoc{lof}}
\newcommand{\borderlof}{
			\listoffigures
			\newpage
}
\makeatother
\fi
%-----------------------------------
%		List of Tables Page
%-----------------------------------

\makeatletter
\def\listoftables{\section*{\centering \Large List of Tables}\@starttoc{lot}}
\newcommand{\borderlot}{		
			\listoftables
			\newpage
}
\makeatother


%-----------------------------------
%		Chapter Head settings
%-----------------------------------
\makeatletter
\renewcommand{\@makechapterhead}[1]{%
	\vspace*{10\p@}%
  	{\parindent \z@ \raggedleft \normalfont
    	\ifnum \c@secnumdepth >\m@ne
        	\huge\bfseries \@chapapp\space \textbf{\thechapter}
        	\par\nobreak
        	\vskip 20\p@
    	\fi
    	\interlinepenalty\@M
    	\Huge \bfseries \textbf{#1}\par\nobreak
    	\vskip 40\p@
  	}
}
\makeatother

%-----------------------------------
%		Table1(Admin) Page
%-----------------------------------

\makeatletter
\newcommand{\putTableAdmin}[1]{
		\newgeometry{vmargin={1.54cm,1.54cm},hmargin={3.17cm,3.17cm}}
		\begin{titlepage}
%			\pagenumbering{roman}
%	    	\setcounter{page}{2}		
			\begin{landscape}
%			\setlength{\textwidth}{9.7in}
%			\setlength{\textheight}{6.3in}
				\begin{center}
					\begin{LARGE}
						\expandafter\uline\expandafter{TABLE I : Details of the Seminars -- Administrative}
					\end{LARGE}
					\\ \vspace*{15pt}
					%\begin{large}
					{#1}
					%\end{large}
				\end{center}
			\end{landscape}
		\end{titlepage}
		\restoregeometry
			\newpage
}
\makeatother

%-----------------------------------
%Table2(Technical) Page
%-----------------------------------

\makeatletter
\newcommand{\putTableTech}[1]{
		%\newgeometry{vmargin={1.54cm,1.54cm},hmargin={3.17cm,3.17cm}}
		%\begin{titlepage}
		  	\setcounter{page}{3}
%			\hspace*{10pt}\parbox{0.90\textwidth}{
				\begin{center}
					\begin{LARGE}
						\expandafter\uline\expandafter{TABLE II : Details of the Seminars -- Technical}
					\end{LARGE}
					\\ \vspace*{35pt}
					%\begin{large}
					{#1}
					%\end{large}
				\end{center}
%			}
		%\end{titlepage}
%		\restoregeometry
			\newpage
}
\makeatother

%-----------------------------------
%		Decleration Page
%-----------------------------------

\makeatletter
\newcommand{\putdecleration}{
\hspace*{10pt}\parbox{0.90\textwidth}{

            
		\begin{center}
                \timesnr{
				\parbox{0.85\textwidth}{
					\centering
					\textbf{
						\LARGE
						\textcolor{black}{\expandafter\uppercase\expandafter{SARDAR VALLABHBHAI NATIONAL INSTITUTE OF TECHNOLOGY,\newline  SURAT}}
						\normalsize
					}
				}
			} \\ \vspace*{40pt}

			\Large
				\underline{\textbf{DECLARATION}}
			\normalsize
		\end{center}
		\vspace*{20pt}
		\centuryf{	
				%\small
				\setstretch{2.5}
				\hspace*{15pt} I hereby declare that the work being presented in this dissertation entitled ``\expandafter\uline\expandafter{\@title}'' by me i.e. \uline{\@atitle\ }\expandafter\uline\expandafter{\@author}, bearing Admn. No: \expandafter\uppercase\expandafter{\expandafter\uline\expandafter{\@regno}} and submitted to the Department of \@dept\ at \@addressInstN\ \@addressInstD, \@addressInstP; is an authentic record of my own work carried out during the period\expandafter\uppercase\expandafter{\expandafter\uline\expandafter{\@semester}} of July 2025 to June 2026 under the supervision of \expandafter\uline\expandafter{\@stitleI\ }\expandafter\uline\expandafter{\@supervisorI}. The matter presented in this report has not been submitted by me in any other University/Institute for any cause. \newline \
		\hspace*{20pt} Neither the source code there in nor the content of the project report have been copied or downloaded from any other source. I understand that my result grades would be revoked if later it is found to be so.\\ \hspace*{15pt}
				\vspace*{10pt}		
		}		
		\\
		\makebox[150pt]{\hrulefill}		
		\\
		(\@author)
		\setstretch{1.5}		

		

		

		\begin{minipage}[c]{\textwidth}
			\hfill
			\vspace*{1cm}
		\end{minipage}
		
		\begin{minipage}[l]{0.52\textwidth}
			\hfill
		\end{minipage}		
							
	}
	\newpage
}
\makeatother

%-----------------------------------
%		Certificate Page
%-----------------------------------

\makeatletter
\newcommand{\putcertificate}{
		
		\begin{figure}
			\begin{minipage}[l]{0.2\textwidth}		
				\makebox[150pt] \\ \vspace*{-5pt}				
					\includegraphics[width=.7\textwidth]{\@instlogo} 
			\end{minipage}				
			\begin{minipage}[r]{0.8\textwidth}		
				\centuryf{			
					\textbf{				
						\makebox[150pt] \\ \vspace*{-5pt}
							\begin{flushleft}
								Sardar Vallabhbhai National Institute of Technology,\\
								Surat-395007, Gujarat, India
							\end{flushleft}
					}				
				}			
			\end{minipage}		
		\end{figure}	

		\begin{center}
			\Large
				\centuryf{
					\underline{
						\textbf{
							\uppercase{c\ e\ r\ t\ i\ f\ i\ c\ a\ t\ e}
						}
					}
				}
			\normalsize
		\end{center}
		\vspace*{20pt}		
		\centuryf{					
			\textbf{					
				\hspace*{20pt}This is to certify that the dissertation report entitled ``\expandafter\uppercase\expandafter{\expandafter\uline\expandafter{\@title}}'' is prepared and presented by \uline{\@atitle\ }\expandafter\uppercase\expandafter{\expandafter\uline\expandafter{\@author}} bearing Roll No: \expandafter\uppercase\expandafter{\expandafter\uline\expandafter{\@regno}}, 2nd Year of M.Tech (Computer Science And Engineering) and his work is satisfactory.
				\vspace*{150pt} \\
				\Large							
			}
		}

		\normalsize		
		\setstretch{1.5}		
		\begin{minipage}[l]{0.3\textwidth}							
			\centuryf{
				\textbf{			
					\begin{center}
						SUPERVISOR \newline
						\@stitleI \@supervisorI \newline
						\@stitleI \@supervisorII 					
					\end{center}
				}
			}
		\end{minipage}				
		\begin{minipage}[c]{.4\textwidth}						
			\centuryf{
				\textbf{
					\begin{center}								
						JURY \newline \newline 
					\end{center}
				}
			}
		\end{minipage}
		\begin{minipage}[r]{.3\textwidth}									
				\centuryf{
					\textbf{
						\begin{center}					
							HEAD OF DEPT. \newline
							DR. SANKITA J. PATEL \newline
						\end{center}					
					}
				}					
		\end{minipage}									
	\newpage
}
\makeatother


%----------------------------
%   Student Declaration Page
%----------------------------

\makeatletter
\newcommand{\putstudentdec}{
    
      \begin{center}
      \begin{tabular}{||m{15cm}||}
      \hhline{=}\\
       
			\Huge
				\timesnr{\textbf{\hspace*{100pt} Student Declaration
				    }
				} \\
				\hhline{=} 
	\end{tabular}			
			
			\normalsize
	    \end{center}
	    
		\vspace*{20pt}
		\onehalfspacing
		
		{This is to certify that the work described in this project report has been actually carried out and implemented by me}
		
		\begin{center} 
\begin{tabular}{ | m{3cm} | m{5cm} | m{5cm} | } 
\hline
\textbf{Sr.} & \textbf{Admission No.} & \textbf{Student Name} \\ 
\hline
1 & \@regno & \@author \\ 
\hline
\end{tabular}
\end{center}
            
       
       {Neither the source code therein nor the content of the report has been copied or downloaded from any other source. I understand that our result grades would be revoked if later it is found to be so.}
       
       \vspace*{20pt}
       
       \textbf{Signature of the Student: }
       \begin{center}
\begin{tabular}{ | m{3cm} | m{5cm}| m{5cm} | } 
\hline
\textbf{Sr.} & \textbf{Student Name} & \textbf{Student Signature} \\ 
\hline
1 & \@author &  \\ 
\hline
\end{tabular}
\end{center}
		
	
		
\newpage
}
\makeatother

%-----------------------------------
%	New Certificate Page
%-----------------------------------

\makeatletter
\newcommand{\putnewcertificate}{

\begin{center}
	\Large
	\underline{\textbf{C\ E\ R\ T\ I\ F\ I\ C\ A\ T\ E}}
	\normalsize
\end{center}

\vspace*{10pt}

\Large		
\onehalfspacing		
\setstretch{1.5}					

\vspace*{10pt}

\normalsize\timesnr{
This is to certify that the dissertation report entitled 
``\expandafter\uline\expandafter{\@title}'', prepared and presented by 
\uline{\@atitle\ }\expandafter\uline\expandafter{\@author}, 
bearing Admn. No: 
\expandafter\uppercase\expandafter{\expandafter\uline\expandafter{\@regno}} 
of M.Tech. Semester-IV in Computer Science and Engineering/Computer Science and Engineering with specialization in Information Security and Privacy/ Computer Science and Engineering with specialization in Data Science, 
Department of Computer Science and Engineering, 
Sardar Vallabhbhai National Institute of Technology, Surat 
is satisfactory.
}

\vspace*{50pt}

% =====================================================
% CERTIFIED BY SECTION
% =====================================================

\begin{minipage}[t]{0.48\textwidth}

\Large \textbf{Certified By}
\vspace{30pt}


\small

\centuryf{
\textbf{
\makebox[150pt]{\hrulefill} \\ \vspace*{-5pt}
\@stitleI\ \@supervisorI \\ \vspace*{-5pt}
Professor (HAG), \\ \vspace*{-5pt}
Department of Computer \\ \vspace*{-5pt}
Science and Engineering, \\ \vspace*{-5pt}
Sardar Vallabhbhai National \\ \vspace*{-5pt}
\@addressInstD, \\ \vspace*{-5pt}
\@addressInstP\ -- 395007, Gujarat \\ \vspace*{-5pt}
India
}
}

\end{minipage}
\hfill
\begin{minipage}[t]{0.48\textwidth}

\vspace{50pt}

\small

\centuryf{
\textbf{
\makebox[150pt]{\hrulefill} \\ \vspace*{-5pt}
\@stitleII\ \@supervisorII \\ \vspace*{-5pt}
Solutions Architect, \\ \vspace*{-5pt}
Qorix, \\ \vspace*{-5pt}
Germany
}
}

\end{minipage}

\vspace*{70pt}

% =====================================================
% JURY SIGNATURE
% =====================================================

\begin{minipage}[t]{0.48\textwidth}

\centuryf{
\textbf{
\makebox[150pt]{\hrulefill} \\ \vspace*{-5pt}
Jury's Signature
}
}

\end{minipage}

\vspace*{70pt}

% =====================================================
% PG INCHARGE AND HOD
% =====================================================

\begin{minipage}[t]{0.48\textwidth}

\centuryf{
\textbf{
\makebox[150pt]{\hrulefill} \\ \vspace*{-5pt}
PG Incharge, \\ \vspace*{-5pt}
M.Tech in Computer \\ \vspace*{-5pt}
Science and Engineering, \\ \vspace*{-5pt}
SVNIT - \@addressInstP
}
}

\end{minipage}
\hfill
\begin{minipage}[t]{0.48\textwidth}

\centuryf{
\textbf{
\makebox[150pt]{\hrulefill} \\ \vspace*{-5pt}
Head, \\ \vspace*{-5pt}
Department of Computer \\ \vspace*{-5pt}
Science and Engineering, \\ \vspace*{-5pt}
SVNIT - \@addressInstP
}
}

\end{minipage}

\newpage
}
\makeatother

%-----------------------------------
%		Acknowledgement Page
%-----------------------------------

\makeatletter
\newcommand{\putsvnitack}[1]{
	\hspace*{10pt}\parbox{0.90\textwidth}{
		\begin{center}
			\Large
				\timesnr{
					\textbf{
						Acknowledgments
					}
				}
			\normalsize				
		\end{center}

		\vspace*{20pt}

		\hspace*{20pt} \timesnr{I am grateful to \expandafter\uline\expandafter{\@stitleI\ }\expandafter\uline\expandafter{\@supervisorI}, who has been a great advisor from the very beginning. I am thankful to him for his valuable discussions and the numerous contributions that he has provided to this work. Without his support and guidance, this work could not have been accomplished. Besides my advisor, I would like to thank my research progress committee members for their encouragement, insightful comments, and suggestions.} 

		
		\newline \\
		\hspace*{20pt} I want to thank \expandafter\uline\expandafter{\@hodtitle\ }\expandafter\uline\expandafter{\@hodname}, Head of Computer Science and Engineering, SVNIT, Surat; for providing infrastructural facilities for my work. I want to thank all the faculties and staff members of the Computer Science and Engineering Department, SVNIT, Surat.
    
    
		
		
			
		\begin{flushright}
			\vspace{60pt}  
				\textbf{
					\@author	\\
					\@regno
				}
		\end{flushright}
	}	
	\newpage
}
\makeatother

%-----------------------------------
%		Abstract Page
%-----------------------------------

\makeatletter
\newcommand{\putsvnitabstract}[1]{
			% \hspace*{10pt}\parbox{0.90\textwidth}{
				\begin{center}
					\Large
						\timesnr{
							\textbf{
								{
									Abstract
								}
							}
						}				
				\end{center}
				\vspace*{40pt}
				{#1}

%             \onehalfspacing
% \large
% \timesnr{\it Cellular V2X, the “Vehicle to Everything” standard,
% defines a framework for information exchange among vehicles and other network entities. In one of the main modes, LTE
% V2X relies on a central scheduler to minimize the consumed
% resources in a conflict-free manner.
% It is very difficult to establish and maintain end-to-
% end connections in a vehicle ad hoc network (VANET) as a result
% of high vehicle speed, long inter-vehicle distance, and varying
% vehicle density. Instead, a store-and-forward strategy has been considered for vehicle communications.
% Routing in C-V2X, can be done by  using machine learning technique  which will give us optimal result. }
% \vspace*{20pt}

% \it{ \textbf{Keywords: }{C-V2X, Vehicular Routing, Intelligent Transportation System, Optimal Routing, VANETs.}}
    
			% }	
			\newpage
		}
\makeatother

%-----------------------------------
%		Place bibliography in table of contents
%-----------------------------------
\def\thebibliography#1{\cleardoublepage\chapter*{\raggedleft ddBibliography}\addcontentsline{toc}{chapter}{Bibliography}\list
  {[\arabic{enumi}]}{\settowidth\labelwidth{[#1]}\leftmargin\labelwidth
    \advance\leftmargin\labelsep
    \usecounter{enumi}}
    \def\newblock{\hskip .11em plus .33em minus .07em}
    \sloppy\clubpenalty4000\widowpenalty4000
    \sfcode`\.=1000\relax}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Approval Sheet
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\makeatletter
\newcommand{\putapprovalSheetDepartment}{

\hspace*{6pt}\parbox{0.98\textwidth}{

		\begin{center}
			\centuryf{
				\textbf{
					\Large
					\textcolor{black}{SARDAR VALLABHBHAI NATIONAL INSTITUTE OF TECHNOLOGY, SURAT }
				}
			} \\ \vspace*{3pt}
			\large
			\textbf{Department of Computer Science and Engineering}\\
			\normalsize ({\@acYear})
			\\ \vspace*{5pt}
			\large
				\underline{\textbf{Approval Sheet}}
			\normalsize
			
		\end{center}
		
		\vspace*{10pt}
		
		\centuryf{	
				%\small
				%\setstretch{2.5} \makebox[400pt]{\hrulefill}
				This is to state that the M.Tech.Dissertation Report entitled \expandafter\uline\expandafter{\@title} \hspace{0.1cm} submitted by \hspace{0.1cm} \uline{\@atitle\ }\expandafter\uline\expandafter{\@author}     (Admission No: \expandafter\uline\expandafter{\@regno}) is approved	for the award of the degree of Master of Technology in Computer Science And Engineering/Computer Science and Engineering with specialization in Information Security and Privacy/ Computer Science and Engineering with specialization in Data Science.			
		}
		\vspace*{25pt}
		\begin{center}
			\centuryf{
				\textbf{
					\large
					\underline{\textbf{Board of Examiners}}
				}
			} \\ \vspace*{8pt}
			\normalsize \textbf{Examiners}
			
			\\ \vspace*{15pt}
			
			\makebox[250pt]{\hrulefill} \\
			\makebox[250pt]{\hrulefill}
			
			\\ \vspace*{15pt}
			
			\textbf{Supervisor}
			\\ \vspace*{10pt}
			\makebox[250pt]{\hrulefill} \\
			\\ \vspace*{10pt}
			
			
			\\ \vspace*{10pt}
			\textbf{Head, Department of Computer Science and Engineering}
			\\ \vspace*{10pt}
			\makebox[250pt]{\hrulefill} \\
			\\ \vspace*{10pt}
			
		\end{center}
		
		Date:\makebox[90pt]{\hrulefill}\\
		Place:\makebox[90pt]{\hrulefill}
		
		
	}	
	\newpage
}
\makeatother
%%%%%%%%%%%%%%%%%%%%%%%%%%%
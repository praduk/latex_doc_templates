# Editor-friendly defaults. Resolve paths from this file so an editor can
# invoke latexmk from any template directory.
use Cwd qw(abs_path);
use File::Basename qw(dirname);

my $root = dirname(abs_path(__FILE__));
my $sep = ($^O eq 'MSWin32') ? ';' : ':';
my $old_texinputs = $ENV{'TEXINPUTS'} // '';
my $old_bibinputs = $ENV{'BIBINPUTS'} // '';

$pdf_mode = 4;
$lualatex = 'lualatex %O %S';
$max_repeat = 8;

$ENV{'TEXINPUTS'} = join($sep, '.', "$root/tex//", "$root/templates//", $root, $old_texinputs, '');
$ENV{'BIBINPUTS'} = join($sep, '.', "$root/templates//", $root, $old_bibinputs, '');

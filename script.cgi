#!C:/Strawberry/perl/bin/perl.exe -w


use strict;
use warnings;
use CGI qw(:standard);
use JSON;

use DBI;
use DBD::mysql;
use vars qw($q);

        $q=new CGI;

if(defined $ARGV[0]){
        ajaxRequest($ARGV[0]);
        exit;
}

        if(!param()){
                printHeader();
                printForm();
                printEnd();
                exit;
        }


        if(param()){
                my $button=param('submit') || '';
                if($button eq 'search'){
                        my $searchText=param('searchText');
                        search($searchText);
                        exit;
                }

                if($button eq 'new'){
                        printHeader();
                        printForm("add");
                }
                
                if($button eq 'add'){
                        my $date=param('date');
                        my $time=param('time');
                        my $desc=param('desc');
                        newApp($date,$time,$desc);
                        exit;
                }

                if($button eq 'cancel'){
                        printHeader();
                        printForm();
                        printEnd();
                }

                my $jRequest=param('ajaxrequest');
                if($jRequest){
                        ajaxRequest($jRequest);
                }
        }

sub ajaxRequest{
        
#        open(my $fh, '>', 'c:/users/hthompson/Documents/test.txt') or die "failed    $!";
      
        my $op = JSON -> new -> utf8;
        my $json = $op -> encode({"Date" => "2017-05-08"});
        
        print $json;        

#        print $fh $json;
#        close $fh;
       
}

sub printHeader{
        
print <<END;
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<title>Appointments</title>
<h1>Appointments</h1>
END
        
}        

sub printForm{
        
        my $hiddenFields="";
        my $button="<input type='submit'  name='submit' value='new'>";

        if(defined $_[0] && $_[0] eq "add"){
                $button="<input type='submit'  name='submit' value='add'><input type='submit'  name='submit' value='cancel'>";
                $hiddenFields="<br><br>Date<input type='text' name='date'><br><br>Time<input type='text' name='time'><br><br>Desc<input type='text' name='desc'><br><br><br>";
        }



print <<END;
<body>
<br><br>
<form action="http://localhost/cgi-bin/script.cgi" method="GET">
$button
$hiddenFields
<br><br>
<input type="text" name="searchText">
<input type="submit"  name="submit" value="search">
</form></body>
END
        
}


sub printEnd{

print <<END;
</html>
END

}
sub search{

        my $date;
        my $time;
        my $desc;
        
        my $host="localhost";
        my $db="dbi:mysql:appointments:localhost:3306";
        my $user="hthompson";
        my $passwd="Ranger99";
        my $query;
        
        my $con=DBI->connect($db,$user,$passwd)
                or die $DBI::errstr;

        printHeader();
        printForm();

        if(length $_[0]){
                $query=$con->prepare("Select sch_date,sch_time,sch_desc from schedule where sch_date = ?");
                $query->execute($_[0]);
        }else{
                $query=$con->prepare("Select sch_date,sch_time,sch_desc from schedule");
                $query->execute();
        }
        
        $query->bind_columns(undef,\$date,\$time,\$desc);

        print $q->table($q->Tr($q->th(['Date', 'Time', 'Description'])));

        print "<br>";
        
        while($query->fetch()){                my $value=param('search');

                print $q->Tr($q->td([$date,$time,$desc]));
                print "<br>";
        }
                
        printEnd();
}


sub newApp{
        printHeader();
        printForm("add");
        print "new   $_[0]";

        my $host="localhost";
        my $db="dbi:mysql:appointments:localhost:3306";

        my $user="hthompson";
        my $passwd="Ranger99";

        my $con=DBI->connect($db,$user,$passwd);

        my $stat=$con->prepare("insert into schedule (sch_date,sch_time,sch_desc) values(?,?,?)");

        $stat->execute($_[0],$_[1],$_[2]);

        $con->disconnect;      
}
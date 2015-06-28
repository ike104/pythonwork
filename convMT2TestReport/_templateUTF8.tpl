﻿<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
  <meta http-equiv="Content-Type" 
            content="text/html; charset=UTF-8">
    <title>$$TITLE$$</title>
    <style type="text/css" media="screen">
    <!--
    td { font: 9pt Tahoma,Arial; }
    //-->
    </style>
    <style type="text/css" media="print">
    <!--
    td { font: 7pt Tahoma,Arial; }
    //-->
    </style>
    <style type="text/css">
    <!--
    .msdate { mso-number-format:"General Date"; }
    .mspt   { mso-number-format:\#\,\#\#0\.00;  }
    //-->
    </style>
	
	<style type="text/css">  
	<!-- 
	table.table0 {
	   table-layout: auto;
	   width: 820px;
	   border: 0px; 
	}
	table.table0 td:nth-of-type(1) {
	   text-align: left;
	   font: 20pt Tahoma,Arial;
	}
	table.table0 td:nth-of-type(2) {
	   text-align: center;
	   font: 14pt Tahoma,Arial;
	}
	table.table0 td:nth-of-type(3) {
	   text-align: right;
	   font: 12pt Tahoma,Arial;
	}
	-->  
	</style>  
	<style type="text/css">  
	<!-- 
	table.table1 {
	   width: 820px;
	   text-align: center;  
	   table-layout: auto;     
	   border-collapse: collapse; 
	   border: 1px solid gray;   
	}
	table.table1 td:nth-of-type(1) {
	   border: 1px solid gray; 
	   padding: 3px;            
	   text-align: left;
	}	
	table.table1 td:nth-of-type(2) {
	   border: 1px solid gray; 
	   padding: 3px;           
	   text-align: left;
	}	
	-->  
	</style>  
	<style type="text/css">  
	<!-- 
	.table2 {
	   width: 820px;
	   table-layout: auto;     
	   border-collapse: collapse; 
	   border: 1px solid gray;   
	   height: 8;
	   background-color: #FFFFFF;
	}
	.table2 td:nth-of-type(2n+1) {
	   border: 1px solid gray; 
	   padding: 3px;           
	   text-align: left;
	   background-color: #E0E0E0;
		}
	.table2 td:nth-of-type(2n) {
	   border: 1px solid gray; 
	   padding: 3px;           
	   text-align: right;
		}	
	-->  
	</style>  
  </head>

<!--- $$START_BODY$$ --->
<body topmargin=1 marginheight=1>
<div align=center>

<table class="table0">
<tr>
	<td>$$EANAME$$</td>
	<td>$$TIMEFRAME$$</td>
	<td>$$SIMPERIOD$$</td>
</tr>
</table>

<table class="table1">
<tr>
	<td>$$EAPARAM$$</td>
</tr>
<tr>
	<td><A href="$$HTMLFILE$$">$$HTMLFILE$$</A></td>
</tr>
</table>
<table class="table2">
<tr align=left>
	<td>通貨</td>
	<td>$$SYMBOL$$</td>
	<td>Period</td>
	<td>$$PERIOD$$</td>
	<td>総取引</td>
	<td>$$TOTALTRADE$$</td>
	<td>PF</td>
	<td>$$PF$$</td>
	<td>DD(%)</td>
	<td>$$DD$$</td>
</tr>
<tr align=left>
	<td>勝率(%)</td>
	<td>$$WINRATE$$</td>
	<td>Long勝率(%)</td>
	<td>$$LONGWINRATE$$</td>
	<td>Short勝率(%)</td>
	<td>$$SHORTWINRATE$$</td>
	<td>連勝</td>
	<td>$$CONSECTIVEWINS$$</td>
	<td>連敗</td>
	<td>$$CONSECTIVELOSSES$$</td>
</tr>
</table>
<img src="$$TRADEIMAGE$$" width=820 height=200 border=0 alt="Graph">
</body>
<!--- $$END_BODY$$ --->


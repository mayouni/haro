try
	zip_openfile("never.zip", "w")
catch
	? "refused"
done
? fexists("never.zip")

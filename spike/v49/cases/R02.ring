try
	zip_openfile()
catch
	? cCatchError
done
try
	zip_entry_open()
catch
	? cCatchError
done
try
	zip_entry_write()
catch
	? cCatchError
done
try
	zip_entry_fwrite()
catch
	? cCatchError
done
try
	zip_entry_read()
catch
	? cCatchError
done
try
	zip_entry_fread()
catch
	? cCatchError
done
try
	zip_entry_close()
catch
	? cCatchError
done
try
	zip_extract_allfiles()
catch
	? cCatchError
done
try
	zip_close()
catch
	? cCatchError
done
try
	zip_filescount()
catch
	? cCatchError
done
try
	zip_getfilenamebyindex()
catch
	? cCatchError
done
try
	zip_extract_file()
catch
	? cCatchError
done

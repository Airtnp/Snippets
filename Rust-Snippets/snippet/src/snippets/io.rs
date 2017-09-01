use std::io;

pub fn read_from_stdin(buf: &mut String) -> io::Result<()> {
    try!(io::stdin().read_line(buf));
    Ok(())
}

pub fn write_to_stdout(buf: &[u8]) -> io::Result<()> {
    try!(io::stdout().write(&buf));
    Ok(())
}

// create file and write something
pub fn create_file(filename: &str, buf: &[u8]) -> io::Result<()> {
    let mut f = try!(File::create(filename));
    try!(f.write(&buf));
    Ok(())
}

// read from file to String
pub fn read_file(filename: &str, mut buf: &mut String) -> io::Result<()> {
    let mut f = try!(File::open(filename));
    try!(f.read_to_string(&mut buf));
    Ok(())
}
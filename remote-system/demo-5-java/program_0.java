import java.util.*;
import java.io.*;
public class program {
	static ArrayList<Integer> vlist = new ArrayList<Integer>();
	public static void fillList(){try{Scanner scanner=new Scanner(new File("inputs"));while(scanner.hasNextLine()){vlist.add(Integer.parseInt(scanner.nextLine()));}scanner.close();}catch(FileNotFoundException e){e.printStackTrace();}}
	public static void emptyList()throws IOException{FileWriter fileWriter=new FileWriter("outputs");PrintWriter printWriter=new PrintWriter(fileWriter);for(Integer item:vlist){printWriter.println(item);}printWriter.close();}

	public static void main(String[] args){
		int x = 0;
		fillList();

		for (Integer item: vlist){
			vlist.set(x, item + 1);
			x++;
		}

		try{emptyList();}
		catch (IOException e){}
}}
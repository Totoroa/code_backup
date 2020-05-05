/* new-pdg.sc

   This script returns the dependence(data/control) relationship of each function's lines in the corresponding cpg.
   
   Arguments:
       inFile: The path to the extracted functions, eg: F:/data/self_vul_repo/functions/Bad
       outFile: The path to restore the result, eg: F:/data/self_vul_repo/functions/Bad/BadFunc_lines
   
   Note: How to run this script ?
   (1)You need to parse the functions by joern to generate a cpg: "./joern-parse <directory-to-functions> --out <path-to-store-cpg/name.bin>".
   (2)Enter the joern-cli by "./joern". Then load the cpg generated in (1): "joern> loadCpg(<path-to-store-cpg/name.bin>)"
   (3)Run the script on the loaded cpg.
       joern> cpg.runScript("<path to new_pdg.sc>", Map("inFile"->"inFile-path", "outFile"->"outFile-path"))       
*/

import gremlin.scala.{Edge, GremlinScala}

import io.shiftleft.codepropertygraph.generated.EdgeTypes

import scala.collection.mutable

import java.io.PrintWriter  
import java.io.File  
import scala.reflect.io.Directory 
import scala.collection.mutable.Set 
import java.util.Date

type EdgeEntry = (AnyRef, AnyRef)
type VertexEntry = (AnyRef, String)
type Pdg = (Option[String], List[EdgeEntry], List[VertexEntry])


private def pdgFromEdges(edges: GremlinScala[Edge], filename: String, outFilePath: String): List[EdgeEntry] = {
  val filteredEdges = edges.filter(edge => edge.hasLabel(EdgeTypes.REACHING_DEF, EdgeTypes.CDG)).dedup.l
  //val filteredEdges = edges.dedup.l

  val edgeResult =
    filteredEdges.foldLeft(mutable.Set.empty[EdgeEntry]) {
      case (edgeList, edge) =>
        val edgeEntry = (edge.outVertex().property("LINE_NUMBER").orElse(""), edge.inVertex().property("LINE_NUMBER").orElse(""))
		//val edgeEntry = (edge.inVertex().id, edge.outVertex().id)
        //val inVertexEntry = (edge.inVertex().id, edge.inVertex().property("LINE_NUMBER").orElse(""))
		//val inVertexEntry = (edge.inVertex().id, edge.inVertex().property("CODE").orElse(""))
        //val outVertexEntry = (edge.outVertex().id, edge.outVertex().property("LINE_NUMBER").orElse(""))
		//val outVertexEntry = (edge.outVertex().id, edge.outVertex().property("CODE").orElse(""))

        edgeList += edgeEntry
    }
  edgeResult.toList |> outFilePath+"\\"+filename
  
  return edgeResult.toList
}

def subdirs2(dir: File): Array[File] = {
		//val d = dir.listFiles.filter(_.isDirectory)
		val f = dir.listFiles.filter(_.isFile)//.toIterator
		//f ++ d.toIterator.flatMap(subdirs2 _)
		
		return f
	}

// inFile: The path to the extracted functions, eg: F:/data/self_vul_repo/functions/Bad
// outFile: The path to restore the result, eg: F:/data/self_vul_repo/functions/Bad/BadFunc_lines
@main def main(inFile: String, outFile: String): Unit = {
	//val it = subdirs2(new File("F:\\data\\self_vul_repo\\functions\\Bad"))
	val it = subdirs2(new File(inFile))
	var start_time =new Date().getTime
	for(d <- it){
		val fileName = d.getName()
		val methodName = d.getName().split("\\$",0)(2).dropRight(2)
		println(methodName)
		try{
		  cpg.method(methodName).l.map{method =>
          val edgeEntries = pdgFromEdges(method.asScala.out().flatMap(_.asScala.outE()), fileName, outFile)
		  }
		}catch {
        case ex: Exception => println("error message:" + ex.getMessage)
      }
	}
	var end_time =new Date().getTime
	var runTime = (end_time - start_time)/1000.0
	println("runTime: " + runTime + " s")
}
